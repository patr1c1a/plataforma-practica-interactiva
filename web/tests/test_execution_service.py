import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch

from web.app.services.execution import _run_sandboxed_unittest, run_tests


class TestExecutionService(unittest.TestCase):
    def test_returns_syntax_error_for_invalid_code(self) -> None:
        result = run_tests(
            category="numeros",
            function_name="menor",
            user_code="def menor(",
        )

        self.assertEqual(result["status"], "syntax_error")
        self.assertIn("Error de sintaxis", result["raw_output"])

    def test_blocks_import_statements(self) -> None:
        result = run_tests(
            category="numeros",
            function_name="menor",
            user_code=(
                "def menor(numero1, numero2):\n"
                "    import math\n"
                "    return numero1\n"
            ),
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("No está permitido importar", result["raw_output"])

    def test_requires_target_function_to_exist(self) -> None:
        result = run_tests(
            category="numeros",
            function_name="menor",
            user_code=(
                "def otra_funcion(a, b):\n"
                "    return a\n"
            ),
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("Debe definir la función 'menor'", result["raw_output"])

    def test_rejects_dunder_attribute_access(self) -> None:
        result = run_tests(
            category="numeros",
            function_name="menor",
            user_code=(
                "def menor(numero1, numero2):\n"
                "    return numero1.__class__\n"
            ),
        )

        self.assertEqual(result["status"], "error")
        self.assertIn("atributos internos", result["raw_output"])

    def test_blocks_local_sandbox_in_production_by_default(self) -> None:
        with (
            patch("web.app.services.execution.SANDBOX_PROVIDER", "local"),
            patch("web.app.services.execution.ALLOW_LOCAL_IN_PRODUCTION", False),
            patch("web.app.services.execution._is_production_environment", return_value=True),
            patch("web.app.services.execution._run_local_unittest") as run_local_mock,
        ):
            result = _run_sandboxed_unittest(
                tmp_path=Path("."),
                category="numeros",
                function_name="menor",
            )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "error")
        self.assertIn("no está permitido en producción", result["raw_output"].lower())
        run_local_mock.assert_not_called()

    def test_allows_local_sandbox_in_production_with_explicit_override(self) -> None:
        with (
            patch("web.app.services.execution.SANDBOX_PROVIDER", "local"),
            patch("web.app.services.execution.ALLOW_LOCAL_IN_PRODUCTION", True),
            patch("web.app.services.execution._is_production_environment", return_value=True),
            patch(
                "web.app.services.execution._run_local_unittest",
                side_effect=subprocess.TimeoutExpired(cmd="python", timeout=10),
            ),
        ):
            result = _run_sandboxed_unittest(
                tmp_path=Path("."),
                category="numeros",
                function_name="menor",
            )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["status"], "timeout")


if __name__ == "__main__":
    unittest.main()
