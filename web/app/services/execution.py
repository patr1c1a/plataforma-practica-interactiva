import shutil
import subprocess
import tempfile
import ast
from pathlib import Path


def run_tests(category: str, function_name: str, user_code: str) -> str:
    base_content = Path("content/python/ESP")

    src_file = base_content / "src" / f"{category}.py"
    test_file = base_content / "tests" / f"tests_{category}.py"

    if not src_file.exists() or not test_file.exists():
        return {
            "status": "error",
            "raw_output": "Error interno: categoría o archivo de tests no encontrados.",
        }

    try:
        ast.parse(user_code)
    except SyntaxError as syntax_error:
        formatted_error_message = (
            f"Error de sintaxis en la línea {syntax_error.lineno}:\n"
            f"{syntax_error.msg}"
        )

        return {
            "status": "syntax_error",
            "raw_output": formatted_error_message,
        }
    
    with tempfile.TemporaryDirectory(dir=Path("runtime/tmp")) as tmp_dir:
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
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "raw_output": "La ejecución excedió el tiempo límite.",
            }

        raw_output = result.stdout + "\n" + result.stderr

        if "FAILED" in raw_output:
            status = "fail"
        elif "OK" in raw_output:
            status = "pass"
        else:
            status = "error"

        return {
            "status": status,
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
        node
        for node in user_submitted_ast.body
        if isinstance(node, ast.FunctionDef)
    ]

    if not user_function_definitions:
        raise ValueError("El código enviado no contiene una definición de función válida.")

    user_function_node = user_function_definitions[0]

    updated_module_body = []

    for node in original_module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == target_function_name:
            updated_module_body.append(user_function_node)
        else:
            updated_module_body.append(node)

    original_module_ast.body = updated_module_body

    updated_module_code = ast.unparse(original_module_ast)

    return updated_module_code
