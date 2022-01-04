import unittest
from unittest.case import skip
import requests
import json

API_URL = "http://localhost:7000"


class TestSearch(unittest.TestCase):
    @skip
    def testSearchText(self):
        url = API_URL + "/search"
        data = {"text": "Alt News", "query_type": "text"}
        files = {
            "data": json.dumps(data),
        }
        response = requests.post(url, files=files)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.json()["vector_representation"]), 768)

    def testSearchImage(self):
        url = API_URL + "/search"
        data = {"query_type": "image"}
        files = {
            "media": open("sample_data/image-with-text.jpg", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, files=files)
        print(response.json())
        self.assertEqual(response.status_code, 200)

    @skip
    def testIndexVideo(self):
        url = API_URL + "/search"
        data = {}
        files = {
            "media": open("sample_data/cat_vid_2mb.mp4", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, files=files)
        print(response.json())
        self.assertEqual(response.status_code, 200)
