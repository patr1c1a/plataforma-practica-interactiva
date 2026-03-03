import tempfile
import unittest
from pathlib import Path

from web.app.services.exercise_repository import (
    CategoryNotFoundError,
    ExerciseRepository,
    FunctionNotFoundError,
)


class TestExerciseRepository(unittest.TestCase):
    def test_raises_when_category_does_not_exist(self) -> None:
        repository = ExerciseRepository(base_exercises_path=Path("content/python/ESP/src"))

        with self.assertRaises(CategoryNotFoundError):
            repository.get_function_details("categoria_inexistente", "f")

    def test_raises_when_function_does_not_exist(self) -> None:
        repository = ExerciseRepository(base_exercises_path=Path("content/python/ESP/src"))

        with self.assertRaises(FunctionNotFoundError):
            repository.get_function_details("numeros", "funcion_inexistente")

    def test_returns_docstring_and_signature(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base_path = Path(tmp_dir)
            module_path = base_path / "demo.py"
            module_path.write_text(
                (
                    "def prueba(a, b):\n"
                    "    \"\"\"Descripcion breve.\"\"\"\n"
                    "    return a + b\n"
                ),
                encoding="utf-8",
            )

            repository = ExerciseRepository(base_exercises_path=base_path)
            details = repository.get_function_details("demo", "prueba")

            self.assertEqual(details["docstring"], "Descripcion breve.")
            self.assertEqual(details["signature"], "def prueba(a, b):\n    ")


if __name__ == "__main__":
    unittest.main()
