from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from web.app.services.execution import run_tests
import ast

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/exercises")
def list_exercises(request: Request):
    base_path = Path("content/python/ESP/src")
    exercises = {}

    for file_path in base_path.glob("*.py"):
        category = file_path.stem

        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        functions = [
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]

        exercises[category] = functions

    # Si el request viene de HTMX, devuelve HTML
    if request.headers.get("hx-request") == "true":
        return templates.TemplateResponse(
            "fragments/exercise_list.html",
            {
                "request": request,
                "exercises": exercises,
            },
        )

    # Caso contrario, devuelve JSON
    return exercises


@router.get("/exercises/{category}/{function_name}")
def exercise_detail(request: Request, category: str, function_name: str):
    base_path = Path("content/python/ESP/src")
    file_path = base_path / f"{category}.py"

    if not file_path.exists():
        return HTMLResponse(status_code=404, content="Categoría no encontrada")

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    function_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = node
            break

    if function_node is None:
        return HTMLResponse(status_code=404, content="Función no encontrada")

    # Obtener docstring (enunciado)
    docstring = ast.get_docstring(function_node)

    # Obtener firma de la función
    args = [arg.arg for arg in function_node.args.args]
    signature = f"def {function_name}({', '.join(args)}):"

    return templates.TemplateResponse(
        "fragments/exercise_detail.html",
        {
            "request": request,
            "category": category,
            "function_name": function_name,
            "docstring": docstring,
            "signature": signature,
        },
    )


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

