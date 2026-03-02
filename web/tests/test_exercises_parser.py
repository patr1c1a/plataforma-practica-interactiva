import unittest

try:
    from web.app.routers.exercises import parse_problem_description
    HAS_FASTAPI_STACK = True
except ModuleNotFoundError:
    HAS_FASTAPI_STACK = False


@unittest.skipUnless(HAS_FASTAPI_STACK, "fastapi stack is not installed")
class TestExerciseProblemDescriptionParser(unittest.TestCase):
    def test_parse_complete_docstring(self) -> None:
        docstring = """
        Retorna el menor de dos números.
        Ejemplos:
            menor(numero1=3, numero2=1) -> 1
        -Parámetros:
            -numero1 (numérico): primer número.
            -numero2 (numérico): segundo número.
        -Valor retornado:
            (numérico) menor valor entre numero1 y numero2.
        """

        parsed = parse_problem_description(docstring)

        self.assertEqual(
            parsed["description"],
            ["Retorna el menor de dos números."],
        )
        self.assertEqual(len(parsed["examples"]), 1)
        self.assertEqual(parsed["examples"][0]["output"], "1")
        self.assertEqual(len(parsed["parameters"]), 2)
        self.assertEqual(parsed["parameters"][0]["name"], "numero1")
        self.assertEqual(parsed["return_value"]["type"], "numérico")

    def test_parse_empty_docstring(self) -> None:
        parsed = parse_problem_description(None)

        self.assertEqual(parsed["description"], [])
        self.assertEqual(parsed["examples"], [])
        self.assertEqual(parsed["parameters"], [])
        self.assertIsNone(parsed["return_value"])


if __name__ == "__main__":
    unittest.main()
