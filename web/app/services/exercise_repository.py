import ast
import re
from pathlib import Path
from typing import TypedDict

from web.app.services.exercise_catalog import BASE_EXERCISES_PATH


class CategoryNotFoundError(FileNotFoundError):
    pass


class FunctionNotFoundError(LookupError):
    pass


class ExerciseFunctionDetails(TypedDict):
    docstring: str | None
    signature: str


SAFE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ExerciseRepository:
    def __init__(self, base_exercises_path: Path | None = None) -> None:
        self._base_exercises_path = base_exercises_path or BASE_EXERCISES_PATH

    def get_function_details(
        self, category: str, function_name: str
    ) -> ExerciseFunctionDetails:
        if not SAFE_IDENTIFIER_PATTERN.fullmatch(category):
            raise CategoryNotFoundError(category)
        if not SAFE_IDENTIFIER_PATTERN.fullmatch(function_name):
            raise FunctionNotFoundError(function_name)

        base_path = self._base_exercises_path.resolve()
        file_path = (self._base_exercises_path / f"{category}.py").resolve()
        if base_path not in file_path.parents:
            raise CategoryNotFoundError(category)

        if not file_path.exists():
            raise CategoryNotFoundError(category)

        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        function_node = None
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                function_node = node
                break

        if function_node is None:
            raise FunctionNotFoundError(function_name)

        args = [arg.arg for arg in function_node.args.args]
        function_signature = f"def {function_name}({', '.join(args)}):\n    "

        return {
            "docstring": ast.get_docstring(function_node),
            "signature": function_signature,
        }
