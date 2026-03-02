import unittest

from web.app.services.execution import run_tests


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


if __name__ == "__main__":
    unittest.main()
