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

    def test_parse_suggestion_and_split_return_type(self) -> None:
        docstring = """
        Evalua algo.
        Sugerencia didáctica: dividir el problema en pasos.
        Ejemplos:
            ejemplo() -> ok
        -Parámetros:
            -(int; float) valor: número de entrada.
        -Valor retornado:
            (bool; None) indica si se cumple.
        """

        parsed = parse_problem_description(docstring)

        self.assertEqual(parsed["suggestions"], ["dividir el problema en pasos."])
        self.assertEqual(parsed["parameters"][0]["name"], "valor")
        self.assertEqual(parsed["parameters"][0]["type_parts"], ["int", "float"])
        self.assertEqual(parsed["return_value"]["type_parts"], ["bool", "None"])


    def test_parse_multiline_example_input_as_single_example(self) -> None:
        docstring = """
        Busca el destino correspondiente a un boleto.
        Ejemplos:
            buscar_destino(boletos=[(100, "Buenos Aires"), (110, "Madrid"), (120, "Glasgow")],
                           ciudades=[("Buenos Aires", "Argentina"), ("Glasgow", "Escocia"), ("Liverpool", "Inglaterra"),
                                     ("Madrid", "España")],
                           numero_boleto=100),
            -> "Argentina"
        """

        parsed = parse_problem_description(docstring)

        self.assertEqual(len(parsed["examples"]), 1)
        self.assertEqual(
            parsed["examples"][0]["input"],
            'buscar_destino(boletos=[(100, "Buenos Aires"), (110, "Madrid"), (120, "Glasgow")], ciudades=[("Buenos Aires", "Argentina"), ("Glasgow", "Escocia"), ("Liverpool", "Inglaterra"), ("Madrid", "España")], numero_boleto=100),',
        )
        self.assertEqual(parsed["examples"][0]["output"], '"Argentina"')

    def test_parse_example_with_arrow_on_following_line(self) -> None:
        docstring = """
        Reemplaza símbolos.
        Ejemplos:
            reemplazar_simbolos(cadena="--Esto es 1 frase donde reemplazaremos con @ cada símbolo",
                                nuevo_caracter="@")
            -> "@@Esto es 1 frase donde reemplazaremos con @ cada símbolo"
        """

        parsed = parse_problem_description(docstring)

        self.assertEqual(len(parsed["examples"]), 1)
        self.assertEqual(
            parsed["examples"][0]["input"],
            'reemplazar_simbolos(cadena="--Esto es 1 frase donde reemplazaremos con @ cada símbolo", nuevo_caracter="@")',
        )
        self.assertEqual(
            parsed["examples"][0]["output"],
            '"@@Esto es 1 frase donde reemplazaremos con @ cada símbolo"',
        )


if __name__ == "__main__":
    unittest.main()
