import unittest
from unittest.case import skip
import requests
from requests.exceptions import ConnectTimeout
import json

API_URL = "http://localhost:7000"


class TestSearch(unittest.TestCase):
    @skip
    def testSearchText(self):
        url = API_URL + "/search"
        data = {"text": "Alt News", "query_type": "text"}
        try:
            response = requests.post(url, json=data, timeout=(3.05, 5))
            print(response.json())
            self.assertEqual(response.status_code, 200)
            # self.assertEqual(len(response.json()["vector_representation"]), 768)
        except ConnectTimeout:
            print('Request has timed out')

    @skip
    def testSearchRawQuery(self):
        url = API_URL + "/search"
        data = {"query": "metadata.domain='hate speech'", "query_type": "raw_query"}
        try:
            response = requests.post(url, json=data, timeout=(3.05, 5))
            # print(response.json())
            self.assertEqual(response.status_code, 200)
        except ConnectTimeout:
            print('Request has timed out')

    @skip
    def testSearchImage(self):
        url = API_URL + "/search"
        data = {"query_type": "image"}
        with open("tests/sample_data/people.jpg", "rb") as file:
            data = {"data": json.dumps(data)}
            files = {"media": file}
            try:
                response = requests.post(url, data=data, files=files, timeout=(3.05, 5))
                print(response.text)
                self.assertEqual(response.status_code, 200)
            except ConnectTimeout:
                print('Request has timed out')

    @skip
    def testIndexVideo(self):
        url = API_URL + "/search"
        with open("tests/sample_data/sample-cat-video.mp4", "rb") as file:
            data = {"data": json.dumps({"query_type": "video"})}
            files = {"media": file}
            try:
                response = requests.post(url, data=data, files=files, timeout=(3.05, 5))
                print(response.text)
                self.assertEqual(response.status_code, 200)
            except ConnectTimeout:
                print('Request has timed out')
