from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from web.app.services.execution import run_tests
from web.app.services.exercise_catalog import (
    CATEGORY_TITLES,
    get_exercise_groups,
    get_category_functions,
    get_ordered_category_cards,
)
import ast

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


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
        fragment_template="fragments/exercise_detail.html",
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
        fragment_template="fragments/exercise_detail.html",
        context=template_context,
    )


@router.get("/exercises/{category}/{function_name}")
def exercise_detail(request: Request, category: str, function_name: str):
    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    base_path = Path("content/python/ESP/src")
    file_path = base_path / f"{category}.py"

    if not file_path.exists():
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    function_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = node
            break

    if function_node is None:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    # Get docstring (problem description)
    problem_description = ast.get_docstring(function_node)

    # Get function signature
    args = [arg.arg for arg in function_node.args.args]
    function_signature = f"def {function_name}({', '.join(args)}):\n    "

    template_context = {
        "request": request,
        "category_name": category,
        "function_name": function_name,
        "problem_description": problem_description,
        "function_signature": function_signature,
        "exercise_groups": all_exercises,
        "current_category": category,
        "current_exercise": function_name,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "view": "exercise_detail",
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
