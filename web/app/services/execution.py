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
        updated_code = _replace_function_body(
            original_code,
            function_name,
            user_code,
        )

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



def _replace_function_body(original_code: str, function_name: str, user_code: str) -> str:
    lines = original_code.splitlines()
    new_lines = []

    inside_target = False
    indent = ""

    for line in lines:
        if line.startswith(f"def {function_name}"):
            inside_target = True
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(user_code)
            continue

        if inside_target:
            if line.startswith(indent) and line.strip() != "":
                continue
            else:
                inside_target = False

        new_lines.append(line)

    return "\n".join(new_lines)
