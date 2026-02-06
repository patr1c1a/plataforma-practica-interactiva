from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
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

    # Caso contrario, devuelv JSON
    return exercises
