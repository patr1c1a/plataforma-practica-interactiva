import shutil
import subprocess
import tempfile
import ast
from pathlib import Path

RUNTIME_TMP_DIRECTORY = Path("runtime/tmp")
RUNTIME_TMP_DIRECTORY.mkdir(parents=True, exist_ok=True)

def run_tests(category: str, function_name: str, user_code: str) -> str:
    base_content = Path("content/python/ESP")

    src_file = base_content / "src" / f"{category}.py"
    test_file = base_content / "tests" / f"tests_{category}.py"

    if not src_file.exists() or not test_file.exists():
        return {
            "status": "error",
            "raw_output": "Error interno: categoría o archivo de tests no encontrados.",
        }

    maximum_allowed_code_length = 10_000

    if len(user_code) > maximum_allowed_code_length:
        return {
            "status": "error",
            "raw_output": "El código excede el tamaño máximo permitido.",
        }

    try:
        ast.parse(user_code)

        parsed_user_ast = ast.parse(user_code)
        import_statements = [
            node
            for node in ast.walk(parsed_user_ast)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        if import_statements:
            return {
                "status": "error",
                "raw_output": "No está permitido importar módulos externos.",
            }
    except SyntaxError as syntax_error:
        formatted_error_message = (
            f"Error de sintaxis en la línea {syntax_error.lineno}:\n"
            f"{syntax_error.msg}"
        )

        return {
            "status": "syntax_error",
            "raw_output": formatted_error_message,
        }

    with tempfile.TemporaryDirectory(dir=RUNTIME_TMP_DIRECTORY) as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Same structure as the CLI version
        tmp_src = tmp_path / "src"
        tmp_tests = tmp_path / "tests"
        tmp_src.mkdir()
        tmp_tests.mkdir()

        shutil.copy(src_file, tmp_src / src_file.name)
        shutil.copy(test_file, tmp_tests / test_file.name)

        # Read code
        exercise_path = tmp_src / src_file.name
        original_code = exercise_path.read_text(encoding="utf-8")

        # Replace the function body
        try:
            updated_code = _replace_function_definition(
                original_module_code=original_code,
                target_function_name=function_name,
                user_submitted_code=user_code,
            )
        except ValueError as value_error:
            return {
                "status": "error",
                "raw_output": str(value_error),
            }

        exercise_path.write_text(updated_code, encoding="utf-8")

        # Run tests from root
        timeout_seconds = 10
        try:
            result = subprocess.run(
                [
                    "python",
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
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "raw_output": "La ejecución excedió el tiempo límite.",
            }

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
    user_submitted_code: str,
) -> str:
    original_module_ast = ast.parse(original_module_code)
    user_submitted_ast = ast.parse(user_submitted_code)

    user_function_definitions = [
        node for node in user_submitted_ast.body if isinstance(node, ast.FunctionDef)
    ]
    user_class_definitions = [
        node for node in user_submitted_ast.body if isinstance(node, ast.ClassDef)
    ]

    if not user_function_definitions:
        raise ValueError(
            "El código enviado no contiene una definición de función válida."
        )

    # Separate main function and helpers
    user_functions_by_name = {func.name: func for func in user_function_definitions}

    if target_function_name not in user_functions_by_name:
        raise ValueError(
            f"Debe definir la función '{target_function_name}'."
        )

    updated_module_body = []

    # Replace existing functions if user provided new versions
    for node in original_module_ast.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in user_functions_by_name:
                # Replace with user's version
                updated_module_body.append(user_functions_by_name[node.name])
                # Remove from dict to avoid re-adding later
                del user_functions_by_name[node.name]
            else:
                updated_module_body.append(node)
        else:
            updated_module_body.append(node)

    # Add any new helper functions not originally present
    for remaining_function in user_functions_by_name.values():
        updated_module_body.append(remaining_function)

    # Preserve user-defined helper classes.
    for user_class in user_class_definitions:
        updated_module_body.append(user_class)

    original_module_ast.body = updated_module_body

    return ast.unparse(original_module_ast)
