import ast
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TypedDict

RUNTIME_TMP_DIRECTORY = Path("runtime/tmp")
RUNTIME_TMP_DIRECTORY.mkdir(parents=True, exist_ok=True)

MAXIMUM_ALLOWED_CODE_LENGTH = 10_000
EXECUTION_TIMEOUT_SECONDS = 10

# Names/calls that materially increase sandbox escape risk.
BLOCKED_NAMES = {
    "__import__",
    "eval",
    "exec",
    "compile",
    "open",
    "input",
    "globals",
    "locals",
    "vars",
    "dir",
    "getattr",
    "setattr",
    "delattr",
    "breakpoint",
}

BLOCKED_ATTRIBUTE_NAMES = {
    "__class__",
    "__bases__",
    "__subclasses__",
    "__mro__",
    "__dict__",
    "__globals__",
    "__code__",
    "__closure__",
    "__getattribute__",
}


class ExecutionResult(TypedDict, total=False):
    status: str
    raw_output: str
    failed_cases: list[str]


def _error_result(status: str, message: str) -> ExecutionResult:
    return {
        "status": status,
        "raw_output": message,
    }


def _get_call_name(call_node: ast.Call) -> str | None:
    if isinstance(call_node.func, ast.Name):
        return call_node.func.id
    if isinstance(call_node.func, ast.Attribute):
        return call_node.func.attr
    return None


def _validate_user_submission(
    parsed_user_ast: ast.Module,
    target_function_name: str,
) -> ExecutionResult | None:
    for node in parsed_user_ast.body:
        if isinstance(node, ast.ClassDef):
            return _error_result(
                "error",
                "No se permiten clases en la resolución.",
            )
        if not isinstance(node, ast.FunctionDef):
            return _error_result(
                "error",
                "Solo se permiten definiciones de funciones.",
            )
        if node.decorator_list:
            return _error_result(
                "error",
                "No se permiten decoradores en el código enviado.",
            )

    user_function_names = {
        node.name for node in parsed_user_ast.body if isinstance(node, ast.FunctionDef)
    }
    if not user_function_names:
        return _error_result(
            "error",
            "El código enviado no contiene una definición de función válida.",
        )
    if target_function_name not in user_function_names:
        return _error_result(
            "error",
            f"Debe definir la función '{target_function_name}'.",
        )

    for node in ast.walk(parsed_user_ast):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return _error_result(
                "error",
                "No está permitido importar módulos externos.",
            )

        if isinstance(node, (ast.Global, ast.Nonlocal, ast.Lambda)):
            return _error_result(
                "error",
                "Se detectaron construcciones no permitidas en el código enviado.",
            )

        if isinstance(node, ast.Name):
            if node.id in BLOCKED_NAMES:
                return _error_result(
                    "error",
                    f"No está permitido usar '{node.id}'.",
                )
            if node.id.startswith("__"):
                return _error_result(
                    "error",
                    "No está permitido usar identificadores especiales.",
                )

        if isinstance(node, ast.Attribute):
            if node.attr in BLOCKED_ATTRIBUTE_NAMES or node.attr.startswith("__"):
                return _error_result(
                    "error",
                    "No está permitido acceder a atributos internos.",
                )

        if isinstance(node, ast.Call):
            call_name = _get_call_name(node)
            if call_name in BLOCKED_NAMES:
                return _error_result(
                    "error",
                    f"No está permitido usar '{call_name}'.",
                )

    return None


def run_tests(category: str, function_name: str, user_code: str) -> ExecutionResult:
    base_content = Path("content/python/ESP")

    src_file = base_content / "src" / f"{category}.py"
    test_file = base_content / "tests" / f"tests_{category}.py"

    if not src_file.exists() or not test_file.exists():
        return _error_result(
            "error",
            "Error interno: categoría o archivo de tests no encontrados.",
        )

    if len(user_code) > MAXIMUM_ALLOWED_CODE_LENGTH:
        return _error_result(
            "error",
            "El código excede el tamaño máximo permitido.",
        )

    try:
        parsed_user_ast = ast.parse(user_code)
    except SyntaxError as syntax_error:
        formatted_error_message = (
            f"Error de sintaxis en la línea {syntax_error.lineno}:\n"
            f"{syntax_error.msg}"
        )
        return _error_result("syntax_error", formatted_error_message)

    validation_error = _validate_user_submission(parsed_user_ast, function_name)
    if validation_error:
        return validation_error

    with tempfile.TemporaryDirectory(dir=RUNTIME_TMP_DIRECTORY) as tmp_dir:
        tmp_path = Path(tmp_dir)

        tmp_src = tmp_path / "src"
        tmp_tests = tmp_path / "tests"
        tmp_src.mkdir()
        tmp_tests.mkdir()

        shutil.copy(src_file, tmp_src / src_file.name)
        shutil.copy(test_file, tmp_tests / test_file.name)

        exercise_path = tmp_src / src_file.name
        original_code = exercise_path.read_text(encoding="utf-8")

        try:
            updated_code = _replace_function_definition(
                original_module_code=original_code,
                target_function_name=function_name,
                parsed_user_submitted_ast=parsed_user_ast,
            )
        except ValueError as value_error:
            return _error_result("error", str(value_error))

        exercise_path.write_text(updated_code, encoding="utf-8")

        try:
            result = subprocess.run(
                [
                    "python",
                    "-S",
                    "-B",
                    "-m",
                    "unittest",
                    "-v",
                    f"tests/tests_{category}.py",
                    "-k",
                    f"test_{function_name}",
                ],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT_SECONDS,
                env={
                    **os.environ,
                    "PYTHONIOENCODING": "utf-8",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONNOUSERSITE": "1",
                },
            )
        except subprocess.TimeoutExpired:
            return _error_result(
                "timeout",
                "La ejecución excedió el tiempo límite.",
            )

        raw_output = result.stdout + "\n" + result.stderr

        if result.returncode == 0:
            execution_status = "pass"
        elif "AssertionError" in raw_output:
            execution_status = "fail"
        elif "ImportError" in raw_output:
            execution_status = "error"
        elif "Traceback" in raw_output:
            execution_status = "runtime_error"
        else:
            execution_status = "error"

        failed_test_cases = []

        if execution_status == "fail":
            output_lines = raw_output.splitlines()

            for line in output_lines:
                if line.strip().startswith("AssertionError:"):
                    error_content = line.strip().replace("AssertionError:", "").strip()
                    parts = error_content.split(" : ")

                    comparison_part = parts[0]
                    context_part = parts[1] if len(parts) > 1 else ""

                    if "!=" in comparison_part:
                        actual_value, expected_value = comparison_part.split("!=")
                        formatted_failure = (
                            f"{context_part}\n"
                            f"Esperado: {expected_value.strip()}\n"
                            f"Recibido: {actual_value.strip()}"
                        )
                    else:
                        formatted_failure = error_content

                    failed_test_cases.append(formatted_failure)

        return {
            "status": execution_status,
            "failed_cases": failed_test_cases,
            "raw_output": raw_output,
        }


def _replace_function_definition(
    original_module_code: str,
    target_function_name: str,
    parsed_user_submitted_ast: ast.Module,
) -> str:
    original_module_ast = ast.parse(original_module_code)
    user_submitted_ast = parsed_user_submitted_ast

    user_function_definitions = [
        node for node in user_submitted_ast.body if isinstance(node, ast.FunctionDef)
    ]

    if not user_function_definitions:
        raise ValueError(
            "El código enviado no contiene una definición de función válida."
        )

    user_functions_by_name = {func.name: func for func in user_function_definitions}

    if target_function_name not in user_functions_by_name:
        raise ValueError(f"Debe definir la función '{target_function_name}'.")

    updated_module_body = []

    for node in original_module_ast.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in user_functions_by_name:
                updated_module_body.append(user_functions_by_name[node.name])
                del user_functions_by_name[node.name]
            else:
                updated_module_body.append(node)
        else:
            updated_module_body.append(node)

    for remaining_function in user_functions_by_name.values():
        updated_module_body.append(remaining_function)

    original_module_ast.body = updated_module_body

    return ast.unparse(original_module_ast)
