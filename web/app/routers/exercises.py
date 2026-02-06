from fastapi import APIRouter
from pathlib import Path
import ast

router = APIRouter()


@router.get("/exercises")
def list_exercises():
    base_path = Path("content/python/ESP/src")

    exercises = {}

    for file_path in base_path.glob("*.py"):
        category = file_path.stem  # nombre del archivo sin .py

        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        functions = [
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]

        exercises[category] = functions

    return exercises
