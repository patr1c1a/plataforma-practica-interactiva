import unittest
import subprocess
from pathlib import Path
import sys
from unittest.mock import patch

import web.app.services.execution as execution_module
from web.app.services.execution import (
    _build_user_facing_output,
    _extract_subtests_executed,
    _run_sandboxed_unittest,
    _sanitize_unittest_output,
    run_tests,
)


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

    def test_sanitize_unittest_output_hides_internal_test_names_and_paths(self) -> None:
        raw_output = (
            "test_es_bisiesto (tests.tests_numeros.TestsFuncionesNumeros.test_es_bisiesto) ... FAIL\n"
            "FAIL: test_es_bisiesto (tests.tests_numeros.TestsFuncionesNumeros.test_es_bisiesto)\n"
            "Traceback (most recent call last):\n"
            "  File \"/workspace/tests/tests_numeros.py\", line 93, in test_es_bisiesto\n"
            "    self.assertEqual(es_bisiesto(numero=1900), False)\n"
            "AssertionError: True != False : es_bisiesto(numero=1900)\n"
            "Ran 1 test in 0.005s\n"
            "FAILED (failures=3)\n"
        )

        sanitized = _sanitize_unittest_output(raw_output)

        self.assertNotIn("test_es_bisiesto (tests.tests_numeros", sanitized)
        self.assertNotIn("/workspace/tests/tests_numeros.py", sanitized)
        self.assertNotIn("Ran 1 test", sanitized)
        self.assertIn("AssertionError:", sanitized)
        self.assertIn("FAILED (failures=3)", sanitized)

    def test_sanitize_unittest_output_returns_fallback_message_when_empty(self) -> None:
        raw_output = (
            "test_menor (tests.tests_numeros.TestsFuncionesNumeros.test_menor) ... ok\n"
            "Ran 1 test in 0.003s\n"
            "OK\n"
        )

        sanitized = _sanitize_unittest_output(raw_output)

        self.assertEqual(sanitized, "OK")

    def test_sanitize_unittest_output_hides_subtest_lines_with_argument_context(self) -> None:
        raw_output = (
            "test_mcd_euclides (tests.tests_numeros.TestsFuncionesNumeros.test_mcd_euclides) ...\n"
            "test_mcd_euclides (tests.tests_numeros.TestsFuncionesNumeros.test_mcd_euclides) "
            "(prueba='Argumentos usados: m=60, n=24') ... FAIL\n"
            "test_mcd_euclides (tests.tests_numeros.TestsFuncionesNumeros.test_mcd_euclides) "
            "(prueba='Argumentos usados: m=24, n=60') ... FAIL\n"
            "AssertionError: 24 != 12 : mcd_euclides(m=24, n=60)\n"
            "FAILED (failures=2)\n"
        )

        sanitized = _sanitize_unittest_output(raw_output)

        self.assertNotIn("tests.tests_numeros.TestsFuncionesNumeros", sanitized)
        self.assertNotIn("test_mcd_euclides", sanitized)
        self.assertIn("AssertionError:", sanitized)
        self.assertIn("FAILED (failures=2)", sanitized)

    def test_sanitize_unittest_output_hides_assert_source_lines(self) -> None:
        raw_output = (
            "Traceback (most recent call last):\n"
            "  File \"/workspace/tests/tests_numeros.py\", line 93, in test_es_bisiesto\n"
            "    self.assertEqual(es_bisiesto(numero=1900), False, prueba)\n"
            "AssertionError: True != False : Argumentos usados: numero=1900\n"
            "FAILED (failures=1)\n"
        )

        sanitized = _sanitize_unittest_output(raw_output)

        self.assertNotIn("self.assertEqual(", sanitized)
        self.assertIn("AssertionError:", sanitized)
        self.assertIn("FAILED (failures=1)", sanitized)

    def test_extract_subtests_executed_reads_marker_and_cleans_output(self) -> None:
        raw_output = (
            "SUBTESTS_EXECUTED: 7\n"
            "AssertionError: x != y\n"
            "FAILED (failures=1)\n"
        )

        executed, cleaned = _extract_subtests_executed(raw_output)

        self.assertEqual(executed, 7)
        self.assertNotIn("SUBTESTS_EXECUTED:", cleaned)
        self.assertIn("AssertionError:", cleaned)

    def test_build_user_facing_output_prefixes_executed_tests_count(self) -> None:
        raw_output = (
            "SUBTESTS_EXECUTED: 5\n"
            "AssertionError: True != False\n"
            "FAILED (failures=3)\n"
        )

        user_output = _build_user_facing_output(raw_output)

        self.assertTrue(user_output.startswith("Tests ejecutados: 5"))
        self.assertIn("AssertionError:", user_output)
        self.assertIn("FAILED (failures=3)", user_output)

    @patch("web.app.services.execution.subprocess.run")
    def test_docker_unittest_command_drops_caps_and_sets_no_new_privileges(
        self,
        subprocess_run_mock,
    ) -> None:
        subprocess_run_mock.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr="",
        )

        execution_module._run_docker_unittest(
            tmp_path=Path("."),
            category="numeros",
            function_name="menor",
        )

        command = subprocess_run_mock.call_args.args[0]
        self.assertIn("--cap-drop", command)
        self.assertIn("ALL", command)
        self.assertIn("--security-opt", command)
        self.assertIn("no-new-privileges", command)

    @patch("web.app.services.execution.subprocess.run")
    def test_local_unittest_command_uses_current_python_in_isolated_mode(
        self,
        subprocess_run_mock,
    ) -> None:
        subprocess_run_mock.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr="",
        )

        execution_module._run_local_unittest(
            tmp_path=Path("."),
            category="numeros",
            function_name="menor",
        )

        command = subprocess_run_mock.call_args.args[0]
        self.assertEqual(command[0], sys.executable)
        self.assertIn("-I", command)
        self.assertIn("-S", command)
        self.assertIn("-B", command)

    @patch.dict(
        "web.app.services.execution.os.environ",
        {
            "SECRET_KEY": "top-secret",
            "PYTHONPATH": "custom-path",
            "SYSTEMROOT": r"C:\Windows",
            "TMP": r"C:\Temp",
        },
        clear=True,
    )
    def test_local_subprocess_env_keeps_only_whitelisted_host_variables(self) -> None:
        subprocess_env = execution_module._build_local_subprocess_env()

        self.assertNotIn("SECRET_KEY", subprocess_env)
        self.assertNotIn("PYTHONPATH", subprocess_env)
        self.assertEqual(subprocess_env["SYSTEMROOT"], r"C:\Windows")
        self.assertEqual(subprocess_env["TMP"], r"C:\Temp")
        self.assertEqual(subprocess_env["PYTHONIOENCODING"], "utf-8")
        self.assertEqual(subprocess_env["PYTHONNOUSERSITE"], "1")

    def test_local_preexec_fn_is_disabled_without_local_limits(self) -> None:
        with (
            patch("web.app.services.execution.os.name", "posix"),
            patch("web.app.services.execution.LOCAL_SANDBOX_MAX_MEMORY_BYTES", 0),
            patch("web.app.services.execution.LOCAL_SANDBOX_MAX_FILE_BYTES", 0),
            patch("web.app.services.execution.LOCAL_SANDBOX_MAX_PROCESSES", 0),
            patch("web.app.services.execution.LOCAL_SANDBOX_MAX_CPU_SECONDS", 0),
        ):
            self.assertIsNone(execution_module._build_local_preexec_fn())

    def test_local_preexec_fn_is_disabled_on_windows(self) -> None:
        with patch("web.app.services.execution.os.name", "nt"):
            self.assertIsNone(execution_module._build_local_preexec_fn())


if __name__ == "__main__":
    unittest.main()
