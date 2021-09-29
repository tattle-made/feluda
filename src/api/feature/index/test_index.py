import unittest
from unittest.case import skip
import requests
import json


class TestIndex(unittest.TestCase):
    def testIndexText(self):
        url = "http://localhost:5000/index/text"
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
        print(response.text)
        self.assertEqual(response.status_code, 200)

    @skip
    def testIndexImage(self):
        url = "http://localhost:5000/index/image"
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
        print(response.text)
        self.assertEqual(response.status_code, 200)

    @skip
    def testIndexVideo(self):
        url = "http://localhost:5000/index/video"
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
        print(response.text)
        self.assertEqual(response.status_code, 200)
