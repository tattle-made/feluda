import unittest
from core.server import Server
from .health import HealthController
import requests

server = None


class TestHealth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        health_controller = HealthController()
        server = Server(param={}, controllers=[health_controller], log=None)
        server.start()

    @classmethod
    def tearDownClass(cls):
        server.stop()
        pass

    def testHealthEndpoint(self):
        url = "http://localhost:5000/"
        response = requests.get(url)
        assert response.status_code is 200
        print("test passed")
