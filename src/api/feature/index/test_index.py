import unittest
import requests
import json


class TestIndex(unittest.TestCase):
    def testPostHealthEndpoint(self):
        url = "http://localhost:5000/post_health"
        data = {
            "post": {"id": "1234"},
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"preserve": True},
        }
        files = {
            "media": open("sample_data/image-with-text.jpg", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, json=data, files=files)
        # print(response.text)
        self.assertEqual(response.status_code, 200)
