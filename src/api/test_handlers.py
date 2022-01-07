import unittest
from core.feluda import Feluda
from endpoint import health


class TestIndexApi(unittest.TestCase):
    def setUp(self) -> None:
        self.feluda = Feluda("config.yml")

    def test_health(self):
        rv = self.app.get("/health")
        print(rv.status_code)
        assert rv.status_code == 200
