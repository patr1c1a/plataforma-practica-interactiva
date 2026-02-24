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


@router.get("/exercises")
def list_exercises(request: Request):
    exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercises)

    request_from_htmx = request.headers.get("hx-request") == "true"

    template_context = {
        "request": request,
        "exercise_groups": exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
    }

    # If it's an HTMX request, return only the fragment
    if request_from_htmx:
        fragment_response = templates.TemplateResponse(
            "fragments/exercise_list.html",
            template_context,
        )
        return fragment_response
    
    # If it's a normal request, return the whole page
    whole_page_response = templates.TemplateResponse(
        "index.html",
        template_context,
    )

    return whole_page_response


@router.get("/exercises/{category}")
def list_category_exercises(request: Request, category: str):
    functions = get_category_functions(category)
    if functions is None:
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    exercises = {category: functions}

    request_from_htmx = request.headers.get("hx-request") == "true"

    template_context = {
        "request": request,
        "exercise_groups": exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
    }

    if request_from_htmx:
        fragment_response = templates.TemplateResponse(
            "fragments/exercise_list.html",
            template_context,
        )
        return fragment_response

    whole_page_response = templates.TemplateResponse(
        "index.html",
        template_context,
    )

    return whole_page_response


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

    request_from_htmx = request.headers.get("hx-request") == "true"

    template_context = {
        "request": request,
        "category_name": category,
        "function_name": function_name,
        "problem_description": problem_description,
        "function_signature": function_signature,
        "exercise_groups": None,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
    }

    # If it's an HTMX request, return only the fragment
    if request_from_htmx:
        fragment_response = templates.TemplateResponse(
            "fragments/exercise_detail.html",
            template_context,
        )
        return fragment_response

    # If it's a normal request, return the whole page
    whole_page_response = templates.TemplateResponse(
        "index.html",
        template_context,
    )

    return whole_page_response


@router.post("/exercises/{category}/{function_name}/run")
def run_exercise(
    request: Request,
    category: str,
    function_name: str,
    code: str = Form(...)
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

