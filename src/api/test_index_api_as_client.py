import unittest
from unittest.case import skip
import requests
import json

API_URL = "http://localhost:7000"


class TestIndex(unittest.TestCase):
    @skip
    def testIndexText(self):
        url = API_URL + "/index"
        data = {
            "post": {
                "id": "1234",
                "media_type": "text",
                "media_url": "https://fs.tattle.co.in/service/kosh/file/b078a8ac-1839-415c-9a08-3361a87e8184",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "reflect", "version": "0.1"},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, json=data, files=files)
        print(len(response.json()["vector_representation"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["vector_representation"]), 768)

    @skip
    def testIndexImage(self):
        url = API_URL + "/index"
        data = {
            "post": {
                "id": "1234",
                "media_type": "image",
                "media_url": "https://fs.tattle.co.in/service/kosh/file/c8709f21-bd7d-4e22-af14-50ad8a429f84",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "reflect", "version": "0.1"},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, json=data, files=files)
        self.assertEqual(response.status_code, 200)

    def testIndexVideo(self):
        url = API_URL + "/index"
        data = {
            "post": {
                "id": "1234",
                "media_type": "video",
                "media_url": "https://fs.tattle.co.in/service/kosh/file/07ba4a2f-c0a2-44ba-96d8-7b4cc94c8ee7",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "store", "version": "0.1"},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, json=data, files=files)
        self.assertEqual(response.status_code, 200)
