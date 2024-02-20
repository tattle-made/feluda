import unittest
import requests


class TestHealth(unittest.TestCase):
    def testHealthEndpoint(self):
        url = "http://localhost:5000/health"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
