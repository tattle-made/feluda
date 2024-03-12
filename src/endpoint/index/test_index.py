import unittest

# from unittest.case import skip
import requests
from requests.exceptions import ConnectTimeout
import json

API_URL = "http://localhost:7000"


class TestIndex(unittest.TestCase):
    def testIndexText(self):
        url = API_URL + "/index/text"
        data = {
            "post": {
                "id": "1234",
                "client_id": "123-12312",
                "text": "this ia sample text ",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            print(response.text)
            self.assertEqual(response.status_code, 200)
        except ConnectTimeout:
            print('Request has timed out')

    def testIndexImage(self):
        url = "http://localhost:5000/index/image"
        data = {
            "post": {
                "id": "1234",
                "client_id": "123-12312",
                "media_url": "http://www.google.com/image",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
        }
        files = {
            "media": open("sample_data/image-with-text.jpg", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            print(response.text)
            self.assertEqual(response.status_code, 200)
        except ConnectTimeout:
            print('Request has timed out')

    def testIndexVideo(self):
        url = API_URL + "/index/video"
        data = {
            "post": {"id": "1234"},
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
        }
        files = {
            "media": open("sample_data/image-with-text.jpg", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            print(response.text)
            self.assertEqual(response.status_code, 200)
        except ConnectTimeout:
            print('Request has timed out')

    def testRepresentText(self):
        url = API_URL + "/represent/text"
        data = {
            "post": {
                "id": "1234",
                "client_id": "123-12312",
                "text": "this is sample text ",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "represent"},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            print(response.text)
            self.assertEqual(response.status_code, 200)
            # assert if the length of the vector is 512
        except ConnectTimeout:
            print('Request has timed out')

    def testRepresentImage(self):
        url = API_URL + "/represent/image"
        data = {
            "post": {
                "id": "1234",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {},
        }
        files = {
            "media": open("sample_data/image-with-text.jpg", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()["representation"]), 512)
        except ConnectTimeout:
            print('Request has timed out')

    def testRepresentVideo(self):
        url = API_URL + "/represent/image"
        data = {
            "post": {
                "id": "1234",
                "client_id": "123-12312",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {},
        }
        files = {
            "media": open("sample_data/cat_water.mp4", "rb"),
            "data": json.dumps(data),
        }
        try:
            response = requests.post(url, json=data, files=files, timeout=(3.05, 5))
            print(response.text)
            self.assertEqual(response.status_code, 200)
            # assert if the length of the vector is 512
            # assert if the second returned parameter is a generator
            # assert if every item in the generator is a vectr of 512 dimension
        except ConnectTimeout:
            print('Request has timed out')
