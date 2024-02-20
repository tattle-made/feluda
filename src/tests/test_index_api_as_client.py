import unittest
from unittest.case import skip
import requests
import json

API_URL = "http://localhost:7000"


class TestIndex(unittest.TestCase):
    @skip
    def testIndexText(self):
        url = API_URL + "/index"
        headers = {"Content-Type": "application/json"}
        # headers = {"Content-Type": "multipart/form-data"}
        data = {
            "post": {
                "id": "1234",
                "media_type": "text",
                "media_url": "https://fs.tattle.co.in/service/kosh/file/b078a8ac-1839-415c-9a08-3361a87e8184",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "store", "version": "0.1"},
        }
        with open("sample_data/simple-text.txt", "rb") as media_file:
            files = {
                "media": media_file,
                "data": json.dumps(data),
            }
            # response = requests.post(url, json=data, files=files, headers=headers)
            response = requests.post(url, json=data, headers=headers)
            print(response.text)
            self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.json()["vector_representation"]), 768)

    # @skip
    def testIndexImage(self):
        url = API_URL + "/index"
        headers = {"Content-Type": "application/json"}
        # headers = {"Content-Type": "multipart/form-data"}
        data = {
            "post": {
                "id": "1234",
                "media_type": "image",
                "media_url": "https://raw.githubusercontent.com/tattle-made/feluda/master/src/api/core/operators/sample_data/people.jpg",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "store", "version": "0.1"},
        }
        with open("sample_data/simple-text.txt", "rb") as media_file:
            files = {
                "media": media_file,
                "data": json.dumps(data),
            }
            response = requests.post(url, json=data, headers=headers)
            # response = requests.post(url, json=data, files=files, headers=headers)
            print(response.text)
            self.assertEqual(response.status_code, 200)

    # @skip
    def testIndexVideo(self):
        url = API_URL + "/index"
        headers = {"Content-Type": "application/json"}
        # headers = {"Content-Type": "multipart/form-data"}
        data = {
            "post": {
                "id": "1234",
                "media_type": "video",
                "media_url": "https://github.com/tattle-made/feluda/raw/master/src/api/core/operators/sample_data/sample-cat-video.mp4",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "store", "version": "0.1"},
        }
        files = {
            # "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        response = requests.post(url, json=data, headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)

    @skip
    def testIndexEnqueueImage(self):
        url = API_URL + "/search"
        # headers = {"Content-Type": "application/json"}
        headers = {"Content-Type": "multipart/form-data"}
        data = {
            "post": {
                "id": "1234",
                "media_type": "image",
                "media_url": "https://raw.githubusercontent.com/tattle-made/feluda/master/src/api/core/operators/sample_data/people.jpg",
                "datasource_id": "asdfasdf-asdfasdf-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "enqueue", "version": "0.1"},
        }
        files = {"data": json.dumps(data)}
        response = requests.post(url, json=data, headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)

    @skip
    def testIndexEnqueueImageJSON(self):
        url = API_URL + "/index"
        data = {
            "post": {
                "id": "0003",
                "media_type": "image",
                "media_url": "https://fs.tattle.co.in/service/kosh/file/c8709f21-bd7d-4e22-af14-50ad8a429f84",
                "datasource_id": "asdfasdf-gggggg-asdf",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "misinformation", "type": ["religion"]},
            "config": {"mode": "store", "version": "0.1"},
        }
        response = requests.post(url, json=data)
        # print(response.json())
        self.assertEqual(response.status_code, 200)
