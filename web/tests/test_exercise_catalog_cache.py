import unittest
from unittest.mock import patch

import web.app.services.exercise_catalog as exercise_catalog


class TestExerciseCatalogCache(unittest.TestCase):
    def setUp(self) -> None:
        # Reset module-level cache before each test.
        exercise_catalog._catalog_cache_signature = None
        exercise_catalog._catalog_cache_data = None

    def test_reuses_cache_when_signature_is_unchanged(self) -> None:
        with patch.object(
            exercise_catalog,
            "_build_catalog_signature",
            return_value=(("numeros.py", 1, 100),),
        ), patch.object(
            exercise_catalog,
            "_build_exercise_groups",
            return_value={"numeros": ["menor"]},
        ) as build_groups_mock:
            first = exercise_catalog.get_exercise_groups()
            second = exercise_catalog.get_exercise_groups()

        self.assertEqual(first, {"numeros": ["menor"]})
        self.assertEqual(second, {"numeros": ["menor"]})
        self.assertEqual(build_groups_mock.call_count, 1)

    def test_rebuilds_cache_when_signature_changes(self) -> None:
        signatures = [
            (("numeros.py", 1, 100),),
            (("numeros.py", 2, 100),),
        ]

        with patch.object(
            exercise_catalog,
            "_build_catalog_signature",
            side_effect=signatures,
        ), patch.object(
            exercise_catalog,
            "_build_exercise_groups",
            side_effect=[
                {"numeros": ["menor"]},
                {"numeros": ["menor", "valor_absoluto"]},
            ],
        ) as build_groups_mock:
            first = exercise_catalog.get_exercise_groups()
            second = exercise_catalog.get_exercise_groups()

        self.assertEqual(first, {"numeros": ["menor"]})
        self.assertEqual(second, {"numeros": ["menor", "valor_absoluto"]})
        self.assertEqual(build_groups_mock.call_count, 2)

    def test_get_category_functions_uses_cached_groups(self) -> None:
        with patch.object(
            exercise_catalog,
            "get_exercise_groups",
            return_value={"numeros": ["menor", "valor_absoluto"]},
        ) as get_groups_mock:
            functions = exercise_catalog.get_category_functions("numeros")

        self.assertEqual(functions, ["menor", "valor_absoluto"])
        self.assertEqual(get_groups_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main()
