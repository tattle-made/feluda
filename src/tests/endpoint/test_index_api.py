import unittest
from unittest.case import skip
from core.feluda import Feluda
from endpoint import index
import json


class TestIndexApi(unittest.TestCase):
    @skip
    def setUp(self) -> None:
        feluda = Feluda("config.yml")
        feluda.set_endpoints([index.endpoint.IndexEndpoint])
        self.app = feluda.server.app.test_client()

    @skip
    def test_index_text_url(self):
        data = {
            "post": {
                "id": "asdfasdf-asdfasdf-asdf",
                "media_type": "text",
                "post_id": "1234",
                "client_id": "123-12312",
                "text": "this is sample text",
            },
            "metadata": {"domain": "hate_speech", "type": ["gender", "caste"]},
            "config": {"mode": "reflect", "version": "0.1"},
        }
        files = {
            "media": open("sample_data/simple-text.txt", "rb"),
            "data": json.dumps(data),
        }
        rv = self.app.post("/index", files=files)
        print(rv.data)
        self.assertEqual(rv.status_code, 200)
