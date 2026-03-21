import os
import re
import time
from collections import deque
from threading import Lock

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from web.app.services.execution import run_tests
from web.app.services.exercise_catalog import (
    CATEGORY_TITLES,
    get_category_functions,
    get_exercise_groups,
    get_ordered_category_cards,
)
from web.app.services.exercise_repository import (
    CategoryNotFoundError,
    ExerciseRepository,
    FunctionNotFoundError,
)
from web.app.services.problem_description_parser import ProblemDescriptionParser

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")
problem_description_parser = ProblemDescriptionParser()
exercise_repository = ExerciseRepository()

PRODUCTION_ENVIRONMENT_NAMES = {"prod", "production"}
TRUST_X_FORWARDED_FOR = (
    os.getenv("TRUST_X_FORWARDED_FOR", "").strip().lower() in {"1", "true", "yes"}
)
TRUSTED_PROXY_IPS = {
    value.strip()
    for value in os.getenv("TRUSTED_PROXY_IPS", "").split(",")
    if value.strip()
}
SAFE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _is_production_environment() -> bool:
    for variable_name in ("APP_ENV", "ENVIRONMENT", "FASTAPI_ENV", "PYTHON_ENV"):
        value = os.getenv(variable_name, "").strip().lower()
        if value in PRODUCTION_ENVIRONMENT_NAMES:
            return True

    return False


def _get_int_env(variable_name: str, default_value: int) -> int:
    raw_value = os.getenv(variable_name)
    if raw_value is None:
        return default_value

    return int(raw_value.strip())


IS_PRODUCTION_ENVIRONMENT = _is_production_environment()
EXECUTION_ENABLED = (
    os.getenv("EXECUTION_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
)
RUN_RATE_LIMIT_WINDOW_SECONDS = _get_int_env("RUN_RATE_LIMIT_WINDOW_SECONDS", 60)
RUN_RATE_LIMIT_MAX_REQUESTS = _get_int_env(
    "RUN_RATE_LIMIT_MAX_REQUESTS",
    8 if IS_PRODUCTION_ENVIRONMENT else 20,
)
RUN_MAX_CONCURRENT_EXECUTIONS = _get_int_env(
    "RUN_MAX_CONCURRENT_EXECUTIONS",
    1 if IS_PRODUCTION_ENVIRONMENT else 4,
)
RUN_RATE_LIMIT_MAX_TRACKED_CLIENTS = _get_int_env(
    "RUN_RATE_LIMIT_MAX_TRACKED_CLIENTS",
    2000 if IS_PRODUCTION_ENVIRONMENT else 5000,
)

_run_rate_limit_lock = Lock()
_run_requests_by_client: dict[str, deque[float]] = {}
_run_inflight_lock = Lock()
_run_inflight_executions = 0


def parse_problem_description(docstring: str | None) -> dict:
    # Backward-compatible wrapper used by existing tests/imports.
    return problem_description_parser.parse(docstring)


def render_with_optional_fragment(
    request: Request,
    full_template: str,
    fragment_template: str,
    context: dict,
):
    """
    If it's an HTMX request, return only the fragment.
    If it's a normal request, return the whole page.
    """
    request_from_htmx = request.headers.get("hx-request") == "true"

    if request_from_htmx:
        return templates.TemplateResponse(request, fragment_template, context)

    return templates.TemplateResponse(request, full_template, context)


def _get_client_identifier(request: Request) -> str:
    remote_host = request.client.host if request.client and request.client.host else "unknown"
    if not TRUST_X_FORWARDED_FOR:
        return remote_host

    # Only trust forwarded headers when the immediate peer is a trusted proxy.
    if remote_host not in TRUSTED_PROXY_IPS:
        return remote_host

    x_forwarded_for = request.headers.get("x-forwarded-for")
    if not x_forwarded_for:
        return remote_host

    first_ip = x_forwarded_for.split(",")[0].strip()
    if not first_ip:
        return remote_host

    return first_ip


def _is_safe_identifier(value: str) -> bool:
    return bool(SAFE_IDENTIFIER_PATTERN.fullmatch(value))


def _cleanup_stale_rate_limit_entries(now: float) -> None:
    cutoff = now - RUN_RATE_LIMIT_WINDOW_SECONDS
    clients_to_remove: list[str] = []

    for client_id, request_times in _run_requests_by_client.items():
        while request_times and request_times[0] <= cutoff:
            request_times.popleft()
        if not request_times:
            clients_to_remove.append(client_id)

    for client_id in clients_to_remove:
        _run_requests_by_client.pop(client_id, None)

    tracked_clients = len(_run_requests_by_client)
    if tracked_clients <= RUN_RATE_LIMIT_MAX_TRACKED_CLIENTS:
        return

    overflow = tracked_clients - RUN_RATE_LIMIT_MAX_TRACKED_CLIENTS
    oldest_clients = sorted(
        _run_requests_by_client.items(),
        key=lambda item: item[1][-1] if item[1] else float("-inf"),
    )[:overflow]
    for client_id, _ in oldest_clients:
        _run_requests_by_client.pop(client_id, None)


def _try_start_execution(client_id: str) -> tuple[bool, int, str | None]:
    now = time.monotonic()
    appended_timestamp = False

    with _run_rate_limit_lock:
        _cleanup_stale_rate_limit_entries(now)
        request_times = _run_requests_by_client.setdefault(client_id, deque())
        cutoff = now - RUN_RATE_LIMIT_WINDOW_SECONDS

        while request_times and request_times[0] <= cutoff:
            request_times.popleft()

        if len(request_times) >= RUN_RATE_LIMIT_MAX_REQUESTS:
            return (
                False,
                429,
                "Demasiadas ejecuciones en poco tiempo. Intenta nuevamente en un minuto.",
            )

        request_times.append(now)
        appended_timestamp = True

    with _run_inflight_lock:
        global _run_inflight_executions
        if _run_inflight_executions >= RUN_MAX_CONCURRENT_EXECUTIONS:
            if appended_timestamp:
                with _run_rate_limit_lock:
                    request_times = _run_requests_by_client.get(client_id)
                    if request_times:
                        try:
                            request_times.pop()
                        except IndexError:
                            pass
            return (
                False,
                503,
                "El servidor esta ocupado procesando otras ejecuciones. Reintenta en unos segundos.",
            )

        _run_inflight_executions += 1

    return True, 200, None


def _finish_execution() -> None:
    with _run_inflight_lock:
        global _run_inflight_executions
        if _run_inflight_executions > 0:
            _run_inflight_executions -= 1


def _reset_run_guards_for_tests() -> None:
    with _run_rate_limit_lock:
        _run_requests_by_client.clear()

    with _run_inflight_lock:
        global _run_inflight_executions
        _run_inflight_executions = 0


@router.get("/exercises")
def list_exercises(request: Request):
    exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercises)

    template_context = {
        "request": request,
        "exercise_groups": exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
        "view": "exercise_list",
        "current_category": None,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_list.html",
        context=template_context,
    )


@router.get("/exercises/{category}")
def list_category_exercises(request: Request, category: str):
    if not _is_safe_identifier(category):
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    functions = get_category_functions(category)
    if functions is None:
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    selected_category_exercises = {category: functions}

    template_context = {
        "request": request,
        "exercise_groups": selected_category_exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
        "view": "exercise_list",
        "current_category": category,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_list.html",
        context=template_context,
    )


@router.get("/exercises/{category}/{function_name}")
def exercise_detail(request: Request, category: str, function_name: str):
    if not _is_safe_identifier(category) or not _is_safe_identifier(function_name):
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    functions = all_exercises.get(category)
    if not functions or function_name not in functions:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    try:
        function_details = exercise_repository.get_function_details(category, function_name)
    except CategoryNotFoundError:
        return HTMLResponse(status_code=404, content="Categoria no encontrada")
    except FunctionNotFoundError:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    problem_description = function_details["docstring"]
    problem_sections = parse_problem_description(problem_description)
    function_signature = function_details["signature"]

    ordered_exercises = [
        (category_name, function)
        for category_name, function_names in all_exercises.items()
        for function in function_names
    ]
    current_exercise = (category, function_name)
    if current_exercise not in ordered_exercises:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    current_index = ordered_exercises.index(current_exercise)
    previous_exercise = ordered_exercises[current_index - 1] if current_index > 0 else None
    next_exercise = (
        ordered_exercises[current_index + 1]
        if current_index < len(ordered_exercises) - 1
        else None
    )

    template_context = {
        "request": request,
        "category_name": category,
        "function_name": function_name,
        "problem_description": problem_description,
        "problem_sections": problem_sections,
        "function_signature": function_signature,
        "exercise_groups": all_exercises,
        "current_category": category,
        "current_exercise": function_name,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "view": "exercise_detail",
        "previous_exercise": previous_exercise,
        "next_exercise": next_exercise,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_detail.html",
        context=template_context,
    )


@router.post("/exercises/{category}/{function_name}/run")
def run_exercise(
    request: Request, category: str, function_name: str, code: str = Form(...)
):
    if not _is_safe_identifier(category) or not _is_safe_identifier(function_name):
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    if not EXECUTION_ENABLED:
        return HTMLResponse(
            status_code=503,
            content="La ejecucion de codigo esta temporalmente deshabilitada.",
        )

    functions = get_category_functions(category)
    if functions is None or function_name not in functions:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    client_id = _get_client_identifier(request)
    can_start, status_code, error_message = _try_start_execution(client_id)
    if not can_start:
        return HTMLResponse(status_code=status_code, content=error_message or "Error")

    try:
        result = run_tests(
            category=category,
            function_name=function_name,
            user_code=code,
        )
    finally:
        _finish_execution()

    return templates.TemplateResponse(
        request,
        "fragments/execution_result.html",
        {
            "request": request,
            "result": result,
        },
    )
