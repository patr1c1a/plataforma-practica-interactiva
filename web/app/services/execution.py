import ast
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TypedDict

RUNTIME_TMP_DIRECTORY = Path("runtime/tmp")
RUNTIME_TMP_DIRECTORY.mkdir(parents=True, exist_ok=True)

MAXIMUM_ALLOWED_CODE_LENGTH = 10_000
EXECUTION_TIMEOUT_SECONDS = 10

SANDBOX_PROVIDER = os.getenv("EXECUTION_SANDBOX_PROVIDER", "docker").strip().lower()
DOCKER_IMAGE = os.getenv(
    "EXECUTION_DOCKER_IMAGE", "plataforma-ejercicios-runner:latest"
).strip()
DOCKER_CPUS_LIMIT = os.getenv("EXECUTION_DOCKER_CPUS", "0.5").strip()
DOCKER_MEMORY_LIMIT = os.getenv("EXECUTION_DOCKER_MEMORY", "128m").strip()
DOCKER_PIDS_LIMIT = os.getenv("EXECUTION_DOCKER_PIDS", "64").strip()
ALLOW_LOCAL_IN_PRODUCTION = (
    os.getenv("EXECUTION_ALLOW_LOCAL_IN_PROD", "").strip().lower() in {"1", "true", "yes"}
)

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
SAFE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ExecutionResult(TypedDict, total=False):
    status: str
    raw_output: str
    failed_cases: list[str]

UNITTEST_RUNNER_FILENAME = "_run_selected_tests.py"
SUBTESTS_EXECUTED_MARKER = "SUBTESTS_EXECUTED:"

UNITTEST_RUNNER_SCRIPT = f"""\
import importlib
import io
import sys
import unittest

category = sys.argv[1]
function_name = sys.argv[2]
module_name = f"tests.tests_{{category}}"
module = importlib.import_module(module_name)
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(module)

def filter_suite(input_suite):
    selected = unittest.TestSuite()
    for item in input_suite:
        if isinstance(item, unittest.TestSuite):
            nested = filter_suite(item)
            if nested.countTestCases():
                selected.addTest(nested)
            continue

        if f".test_{{function_name}}" in item.id():
            selected.addTest(item)

    return selected

selected_suite = filter_suite(suite)

class CountingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subtests_executed = 0

    def addSubTest(self, test, subtest, err):
        self.subtests_executed += 1
        super().addSubTest(test, subtest, err)

stream = io.StringIO()
runner = unittest.TextTestRunner(
    stream=stream,
    verbosity=2,
    resultclass=CountingResult,
)
result = runner.run(selected_suite)

executed = result.subtests_executed if result.subtests_executed > 0 else result.testsRun
sys.stdout.write("{SUBTESTS_EXECUTED_MARKER} {{}}\\n".format(executed))
sys.stdout.write(stream.getvalue())
sys.exit(0 if result.wasSuccessful() else 1)
"""


def _error_result(status: str, message: str) -> ExecutionResult:
    return {
        "status": status,
        "raw_output": message,
    }


def _is_safe_identifier(value: str) -> bool:
    return bool(SAFE_IDENTIFIER_PATTERN.fullmatch(value))


def _is_production_environment() -> bool:
    for variable_name in ("APP_ENV", "ENVIRONMENT", "FASTAPI_ENV", "PYTHON_ENV"):
        value = os.getenv(variable_name, "").strip().lower()
        if value in {"prod", "production"}:
            return True

    return False


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


def _build_unittest_command(category: str, function_name: str) -> list[str]:
    return [
        "python",
        "-S",
        "-B",
        UNITTEST_RUNNER_FILENAME,
        category,
        function_name,
    ]


def _run_local_unittest(tmp_path: Path, category: str, function_name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        _build_unittest_command(category, function_name),
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


def _run_docker_unittest(
    tmp_path: Path,
    category: str,
    function_name: str,
) -> subprocess.CompletedProcess[str]:
    host_workspace_path = str(tmp_path.resolve())
    docker_command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--cpus",
        DOCKER_CPUS_LIMIT,
        "--memory",
        DOCKER_MEMORY_LIMIT,
        "--pids-limit",
        DOCKER_PIDS_LIMIT,
        "--read-only",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=16m",
        "--mount",
        f"type=bind,src={host_workspace_path},dst=/workspace",
        "--workdir",
        "/workspace",
        DOCKER_IMAGE,
        *_build_unittest_command(category, function_name),
    ]

    return subprocess.run(
        docker_command,
        capture_output=True,
        text=True,
        timeout=EXECUTION_TIMEOUT_SECONDS,
    )


def _run_sandboxed_unittest(
    tmp_path: Path,
    category: str,
    function_name: str,
) -> subprocess.CompletedProcess[str] | ExecutionResult:
    if SANDBOX_PROVIDER == "docker":
        try:
            return _run_docker_unittest(tmp_path, category, function_name)
        except FileNotFoundError:
            return _error_result(
                "error",
                (
                    "Docker no está instalado o no está en PATH. "
                    "Para desarrollo local, exporta EXECUTION_SANDBOX_PROVIDER=local."
                ),
            )
        except subprocess.TimeoutExpired:
            return _error_result(
                "timeout",
                "La ejecución excedió el tiempo límite.",
            )

    if SANDBOX_PROVIDER == "local":
        if _is_production_environment() and not ALLOW_LOCAL_IN_PRODUCTION:
            return _error_result(
                "error",
                (
                    "Configuración insegura: EXECUTION_SANDBOX_PROVIDER=local "
                    "no está permitido en producción. Usa docker."
                ),
            )

        try:
            return _run_local_unittest(tmp_path, category, function_name)
        except subprocess.TimeoutExpired:
            return _error_result(
                "timeout",
                "La ejecución excedió el tiempo límite.",
            )

    return _error_result(
        "error",
        (
            "Proveedor de sandbox no soportado. "
            "Usa EXECUTION_SANDBOX_PROVIDER=docker o EXECUTION_SANDBOX_PROVIDER=local."
        ),
    )


def _parse_execution_result(raw_output: str, returncode: int) -> tuple[str, list[str]]:
    if returncode == 0:
        return "pass", []

    if "AssertionError" in raw_output:
        execution_status = "fail"
    elif "ImportError" in raw_output:
        execution_status = "error"
    elif "Traceback" in raw_output:
        execution_status = "runtime_error"
    else:
        execution_status = "error"

    failed_test_cases: list[str] = []
    if execution_status != "fail":
        return execution_status, failed_test_cases

    output_lines = raw_output.splitlines()
    for line in output_lines:
        if not line.strip().startswith("AssertionError:"):
            continue

        error_content = line.strip().replace("AssertionError:", "").strip()
        parts = error_content.split(" : ")

        comparison_part = parts[0]
        context_part = parts[1] if len(parts) > 1 else ""

        if "!=" in comparison_part:
            actual_value, expected_value = comparison_part.split("!=", 1)
            formatted_failure = (
                f"{context_part}\n"
                f"Esperado: {expected_value.strip()}\n"
                f"Recibido: {actual_value.strip()}"
            )
        else:
            formatted_failure = error_content

        failed_test_cases.append(formatted_failure)

    return execution_status, failed_test_cases


def _extract_subtests_executed(raw_output: str) -> tuple[int | None, str]:
    marker_pattern = re.compile(
        rf"^\s*{re.escape(SUBTESTS_EXECUTED_MARKER)}\s*(\d+)\s*$",
        re.MULTILINE,
    )
    match = marker_pattern.search(raw_output)
    if not match:
        return None, raw_output

    executed = int(match.group(1))
    cleaned_output = marker_pattern.sub("", raw_output, count=1)
    return executed, cleaned_output


def _sanitize_unittest_output(raw_output: str) -> str:
    sanitized_lines: list[str] = []

    for line in raw_output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if re.match(
            r"^test_[A-Za-z_]\w* \(tests\.[^)]+\)(?: \([^)]*\))? \.\.\.(?: (ok|FAIL|ERROR))?$",
            stripped,
        ):
            continue

        if re.match(r"^(FAIL|ERROR): test_[A-Za-z_]\w* \(tests\.[^)]+\).*$", stripped):
            continue

        if stripped.startswith("Traceback (most recent call last):"):
            continue

        if re.match(r'^\s*File ".*", line \d+, in .+$', line):
            continue

        if re.match(r"^self\.assert[A-Za-z_]\w*\(.*\)$", stripped):
            continue

        if re.match(r"^Ran \d+ test[s]? in .+$", stripped):
            continue

        sanitized_lines.append(stripped)

    sanitized_output = "\n".join(sanitized_lines).strip()
    if not sanitized_output:
        return "No hay salida adicional."

    return sanitized_output


def _build_user_facing_output(raw_output: str) -> str:
    subtests_executed, cleaned_output = _extract_subtests_executed(raw_output)
    sanitized_output = _sanitize_unittest_output(cleaned_output)

    if subtests_executed is None:
        return sanitized_output

    if sanitized_output == "No hay salida adicional.":
        return f"Tests ejecutados: {subtests_executed}"

    return f"Tests ejecutados: {subtests_executed}\n\n{sanitized_output}"


def run_tests(category: str, function_name: str, user_code: str) -> ExecutionResult:
    if not _is_safe_identifier(category) or not _is_safe_identifier(function_name):
        return _error_result(
            "error",
            "Error interno: identificador de categorÃ­a o funciÃ³n no vÃ¡lido.",
        )

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
        runner_path = tmp_path / UNITTEST_RUNNER_FILENAME
        runner_path.write_text(UNITTEST_RUNNER_SCRIPT, encoding="utf-8")

        execution_result = _run_sandboxed_unittest(tmp_path, category, function_name)
        if isinstance(execution_result, dict):
            return execution_result

        raw_output = execution_result.stdout + "\n" + execution_result.stderr
        execution_status, failed_test_cases = _parse_execution_result(
            raw_output=raw_output,
            returncode=execution_result.returncode,
        )
        user_facing_output = _build_user_facing_output(raw_output)

        return {
            "status": execution_status,
            "failed_cases": failed_test_cases,
            "raw_output": user_facing_output,
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
