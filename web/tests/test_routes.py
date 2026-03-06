import unittest
from unittest.mock import patch

try:
    from fastapi.testclient import TestClient
    from web.app.routers import exercises as exercises_router_module
    from web.main import app
    HAS_FASTAPI_STACK = True
except ModuleNotFoundError:
    HAS_FASTAPI_STACK = False


@unittest.skipUnless(HAS_FASTAPI_STACK, "fastapi stack is not installed")
class TestWebRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        exercises_router_module._reset_run_guards_for_tests()

    def test_health_endpoint(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_security_headers_are_present(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("x-content-type-options"), "nosniff")
        self.assertEqual(response.headers.get("x-frame-options"), "DENY")
        self.assertEqual(
            response.headers.get("referrer-policy"),
            "strict-origin-when-cross-origin",
        )
        self.assertIn(
            "frame-ancestors 'none'",
            response.headers.get("content-security-policy", ""),
        )
        self.assertIn(
            "form-action 'self'",
            response.headers.get("content-security-policy", ""),
        )

    def test_external_assets_use_sri(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'src="https://unpkg.com/htmx.org@1.9.12"',
            response.text,
        )
        self.assertIn(
            'src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"',
            response.text,
        )
        self.assertIn(
            'href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css"',
            response.text,
        )
        self.assertGreaterEqual(response.text.count('integrity="sha384-'), 5)
        self.assertGreaterEqual(response.text.count('crossorigin="anonymous"'), 5)

    def test_exercises_list_endpoint(self) -> None:
        response = self.client.get("/exercises")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Resolver ejercicio", response.text)

    def test_exercise_detail_endpoint(self) -> None:
        response = self.client.get("/exercises/numeros/menor")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ejercicio", response.text)

    def test_category_not_found_returns_404(self) -> None:
        response = self.client.get("/exercises/categoria_inexistente")

        self.assertEqual(response.status_code, 404)
        self.assertIn("Categoria no encontrada", response.text)

    def test_function_not_found_returns_404(self) -> None:
        response = self.client.get("/exercises/numeros/funcion_inexistente")

        self.assertEqual(response.status_code, 404)
        self.assertIn("Funcion no encontrada", response.text)

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

    @patch("web.app.routers.exercises.run_tests")
    def test_run_exercise_endpoint_rate_limit_returns_429(self, run_tests_mock) -> None:
        run_tests_mock.return_value = {
            "status": "pass",
            "failed_cases": [],
            "raw_output": "ok",
        }

        with patch.object(exercises_router_module, "RUN_RATE_LIMIT_MAX_REQUESTS", 1):
            first_response = self.client.post(
                "/exercises/numeros/menor/run",
                data={"code": "def menor(numero1, numero2): return numero1"},
                headers={"x-forwarded-for": "203.0.113.10"},
            )
            second_response = self.client.post(
                "/exercises/numeros/menor/run",
                data={"code": "def menor(numero1, numero2): return numero1"},
                headers={"x-forwarded-for": "203.0.113.10"},
            )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)

    @patch("web.app.routers.exercises.run_tests")
    def test_run_exercise_endpoint_rejects_oversized_body_with_413(self, run_tests_mock) -> None:
        oversized_code = "a" * 70000

        response = self.client.post(
            "/exercises/numeros/menor/run",
            data={"code": oversized_code},
        )

        self.assertEqual(response.status_code, 413)
        run_tests_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
