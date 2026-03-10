import os
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
class TestSecurityRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app, raise_server_exceptions=False)

    def setUp(self) -> None:
        exercises_router_module._reset_run_guards_for_tests()

    def test_rate_limit_cannot_be_bypassed_by_rotating_x_forwarded_for(self) -> None:
        payload = {"code": "def menor(numero1, numero2): return numero1"}

        with (
            patch("web.app.routers.exercises.run_tests") as run_tests_mock,
            patch.object(exercises_router_module, "RUN_RATE_LIMIT_MAX_REQUESTS", 1),
        ):
            run_tests_mock.return_value = {
                "status": "pass",
                "failed_cases": [],
                "raw_output": "ok",
            }
            first_response = self.client.post(
                "/exercises/numeros/menor/run",
                data=payload,
                headers={"x-forwarded-for": "203.0.113.10"},
            )
            second_response = self.client.post(
                "/exercises/numeros/menor/run",
                data=payload,
                headers={"x-forwarded-for": "203.0.113.11"},
            )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(
            second_response.status_code,
            429,
            "Rotating X-Forwarded-For should not reset the per-client run limit.",
        )

    @unittest.skipUnless(
        os.name == "nt",
        "Backslash traversal payload is Windows-specific.",
    )
    def test_category_path_traversal_is_rejected(self) -> None:
        traversal_category = "..%5c..%5c..%5c..%5cweb%5capp%5crouters%5chealth"
        response = self.client.get(
            f"/exercises/{traversal_category}/health_check",
        )

        self.assertIn(
            response.status_code,
            {400, 404},
            "Traversal-like category names must be rejected.",
        )

    def test_untrusted_x_forwarded_proto_does_not_enable_hsts(self) -> None:
        response = self.client.get(
            "/health",
            headers={"x-forwarded-proto": "https"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            response.headers.get("strict-transport-security"),
            "HSTS should not be enabled from untrusted X-Forwarded-Proto.",
        )


if __name__ == "__main__":
    unittest.main()
