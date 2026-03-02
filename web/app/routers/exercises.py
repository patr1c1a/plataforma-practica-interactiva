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
        return templates.TemplateResponse(fragment_template, context)

    return templates.TemplateResponse(full_template, context)


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
    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)

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
    current_index = ordered_exercises.index((category, function_name))
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
    result = run_tests(
        category=category,
        function_name=function_name,
        user_code=code,
    )

    return templates.TemplateResponse(
        "fragments/execution_result.html",
        {
            "request": request,
            "result": result,
        },
    )
