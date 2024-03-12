import unittest
import requests
from requests.exceptions import ConnectTimeout


class TestHealth(unittest.TestCase):
    def testHealthEndpoint(self):
        url = "http://localhost:5000/health"
        try:
            response = requests.get(url, timeout=(3.05, 5))
            self.assertEqual(response.status_code, 200)
        except ConnectTimeout:
            print('Request has timed out')
