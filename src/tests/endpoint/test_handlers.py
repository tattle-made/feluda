import unittest
from core.feluda import Feluda

# from endpoint import health
from unittest.case import skip


class TestIndexApi(unittest.TestCase):
    @skip
    def setUp(self) -> None:
        self.feluda = Feluda("config.yml")

    @skip
    def test_health(self):
        rv = self.app.get("/health")
        print(rv.status_code)
        self.assertEqual(rv.status_code, 200)
