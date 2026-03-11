import io
import os
import zipfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from web.app.routers.exercises import router as exercises_router
from web.app.routers.health import router as health_router
from web.app.services.exercise_catalog import (
    CATEGORY_TITLES,
    get_exercise_groups,
    get_ordered_category_cards,
)

app = FastAPI()
MAX_RUN_REQUEST_BODY_BYTES = int(
    os.getenv("RUN_MAX_REQUEST_BODY_BYTES", "65536")
)
OVERSIZED_RUN_REQUEST_MESSAGE = (
    "El contenido enviado es demasiado grande para ejecutarse. "
)
DEFAULT_CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "script-src 'self' https://unpkg.com https://cdnjs.cloudflare.com; "
    "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
    "img-src 'self' data:; "
    "font-src 'self' https:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)
CONTENT_SECURITY_POLICY = os.getenv(
    "SECURITY_CONTENT_SECURITY_POLICY",
    DEFAULT_CONTENT_SECURITY_POLICY,
).strip()
TRUST_X_FORWARDED_PROTO = (
    os.getenv("TRUST_X_FORWARDED_PROTO", "").strip().lower() in {"1", "true", "yes"}
)
TRUSTED_PROXY_IPS = {
    value.strip()
    for value in os.getenv("TRUSTED_PROXY_IPS", "").split(",")
    if value.strip()
}


class _RequestBodyTooLargeError(Exception):
    """Internal sentinel used to abort oversized streamed request bodies."""


class RunRequestBodyLimitMiddleware:
    def __init__(self, app, max_body_bytes: int):
        self.app = app
        self.max_body_bytes = max_body_bytes

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "")
        path = scope.get("path", "")
        is_run_endpoint = (
            method == "POST"
            and path.startswith("/exercises/")
            and path.endswith("/run")
        )
        if not is_run_endpoint:
            await self.app(scope, receive, send)
            return

        headers = scope.get("headers", [])
        content_length_value = None
        for key, value in headers:
            if key == b"content-length":
                try:
                    content_length_value = int(value.decode("latin-1"))
                except ValueError:
                    content_length_value = None
                break

        if (
            content_length_value is not None
            and content_length_value > self.max_body_bytes
        ):
            response = self._build_oversized_response(scope, receive)
            await response(scope, receive, send)
            return

        received_body_bytes = 0

        async def limited_receive():
            nonlocal received_body_bytes
            message = await receive()

            if message.get("type") == "http.request":
                received_body_bytes += len(message.get("body", b""))
                if received_body_bytes > self.max_body_bytes:
                    raise _RequestBodyTooLargeError()

            return message

        try:
            await self.app(scope, limited_receive, send)
        except _RequestBodyTooLargeError:
            response = self._build_oversized_response(scope, receive)
            await response(scope, receive, send)
            return

    def _build_oversized_response(self, scope, receive):
        request = Request(scope, receive=receive)
        request_from_htmx = request.headers.get("hx-request") == "true"

        if request_from_htmx:
            return templates.TemplateResponse(
                request,
                "fragments/execution_result.html",
                {
                    "request": request,
                    "result": {
                        "status": "error",
                        "failed_cases": [],
                        "raw_output": OVERSIZED_RUN_REQUEST_MESSAGE,
                    },
                },
                status_code=200,
            )

        return StreamingResponse(
            iter([b"Request body too large for code execution endpoint."]),
            status_code=413,
            media_type="text/plain",
        )


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Content-Security-Policy", CONTENT_SECURITY_POLICY)

    remote_host = request.client.host if request.client and request.client.host else ""
    forwarded_proto = ""
    if TRUST_X_FORWARDED_PROTO and (not TRUSTED_PROXY_IPS or remote_host in TRUSTED_PROXY_IPS):
        forwarded_proto = (
            request.headers.get("x-forwarded-proto", "").split(",")[0].strip().lower()
        )

    request_is_https = request.url.scheme == "https" or forwarded_proto == "https"
    if request_is_https:
        response.headers.setdefault(
            "Strict-Transport-Security",
            "max-age=31536000; includeSubDomains",
        )

    return response

# Static files
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.add_middleware(
    RunRequestBodyLimitMiddleware,
    max_body_bytes=MAX_RUN_REQUEST_BODY_BYTES,
)

app.include_router(health_router)
app.include_router(exercises_router)


def _download_offline_folder(language: str) -> StreamingResponse:
    language = language.upper()
    if language not in {"ESP", "ENG"}:
        raise HTTPException(status_code=400, detail="Idioma offline no válido.")

    offline_dir = BASE_DIR.parent / "content" / "python" / language
    if not offline_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró la versión offline {language}.",
        )

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(
        zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as zip_file:
        for file_path in offline_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(offline_dir)
                zip_file.write(
                    file_path,
                    arcname=f"{language}/{relative_path.as_posix()}",
                )

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": (
                f'attachment; filename="plataforma-practica-interactiva-{language}.zip"'
            )
        },
    )


@app.get("/")
def index(request: Request):
    exercise_groups = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercise_groups)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "exercise_groups": exercise_groups,
            "category_cards": category_cards,
            "category_titles": CATEGORY_TITLES,
            "problem_description": None,
            "view": "home",
        },
    )


@app.get("/offline")
def offline_instructions(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "exercise_groups": {},
            "category_cards": [],
            "category_titles": CATEGORY_TITLES,
            "problem_description": None,
            "view": "offline",
            "offline_repo_url": (
                "https://github.com/patr1c1a/plataforma-practica-interactiva/"
                "tree/main/content/python/"
            ),
            "offline_download_esp_url": "/offline/download/esp",
            "offline_download_eng_url": "/offline/download/eng",
        },
    )


@app.get("/offline/download/esp")
def download_offline_esp():
    return _download_offline_folder("ESP")


@app.get("/offline/download/eng")
def download_offline_eng():
    return _download_offline_folder("ENG")


@app.get("/favicon.ico")
def favicon():
    return FileResponse(BASE_DIR / "static" / "favicon.ico")
