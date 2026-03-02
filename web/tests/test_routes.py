import unittest
from unittest.mock import patch

try:
    from fastapi.testclient import TestClient
    from web.main import app
    HAS_FASTAPI_STACK = True
except ModuleNotFoundError:
    HAS_FASTAPI_STACK = False


@unittest.skipUnless(HAS_FASTAPI_STACK, "fastapi stack is not installed")
class TestWebRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_exercises_list_endpoint(self) -> None:
        response = self.client.get("/exercises")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Resolver ejercicio", response.text)

    @patch("web.app.routers.exercises.run_tests")
    def test_run_exercise_endpoint_renders_result_fragment(self, run_tests_mock) -> None:
        run_tests_mock.return_value = {
            "status": "pass",
            "failed_cases": [],
            "raw_output": "ok",
        }

        response = self.client.post(
            "/exercises/numeros/menor/run",
            data={"code": "def menor(numero1, numero2): return numero1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('data-status="pass"', response.text)


if __name__ == "__main__":
    unittest.main()
