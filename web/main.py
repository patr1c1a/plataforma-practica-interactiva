import io
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

# Static files
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

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
                f'attachment; filename="plataforma-ejercicios-{language}.zip"'
            )
        },
    )


@app.get("/")
def index(request: Request):
    exercise_groups = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercise_groups)

    return templates.TemplateResponse(
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
        "index.html",
        {
            "request": request,
            "exercise_groups": {},
            "category_cards": [],
            "category_titles": CATEGORY_TITLES,
            "problem_description": None,
            "view": "offline",
            "offline_repo_url": (
                "https://github.com/programacion-desde-cero/plataforma-ejercicios/"
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
