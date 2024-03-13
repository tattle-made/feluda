import unittest
from core.feluda import Feluda
from endpoint import health
from unittest.case import skip


class TestIndexApi(unittest.TestCase):
    @skip
    def setUp(self) -> None:
        feluda = Feluda("config.yml")
        feluda.set_endpoints([health.HealthEndpoint])
        self.app = feluda.server.app.test_client()

    @skip
    def test_health(self):
        rv = self.app.get("/health")
        print(rv.status_code)
        self.assertEqual(rv.status_code, 200)
