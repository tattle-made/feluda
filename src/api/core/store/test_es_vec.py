import unittest
from unittest.case import skip
import requests
from .es_vec import ES
import pprint
from datetime import datetime
import numpy as np

pp = pprint.PrettyPrinter(indent=4)


class TestES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # ping es server to see if its working
        response = requests.get("http://es:9200")

        if response.status_code is 200:
            print("Elastic search server is running")
        else:
            print("No elasticsearch service found. Tests are bound to fail.")
        cls.param = {
            "host_name": "es",
            "text_index_name": "test_text",
            "image_index_name": "test_image",
            "video_index_name": "test_video",
        }

    @classmethod
    def tearDownClass(cls) -> None:
        print("TEARING DOWN CLASS")
        pass

    # def tearDown(self) -> None:
    #     pass

    @skip
    def test_create_indices(self):
        print(self.param)
        es = ES(self.param)
        es.connect()
        es.create_index()
        indices = es.get_indices()
        # print(indices)

        self.assertEquals(
            indices["test_text"]["mappings"]["properties"]["text"]["analyzer"],
            "standard",
        )
        self.assertEquals(
            indices["test_image"]["mappings"]["properties"]["image_vec"]["dims"], 512
        )
        self.assertEquals(
            indices["test_video"]["mappings"]["properties"]["vid_vec"]["dims"], 512
        )

    @skip
    def test_store_image(self):
        es = ES(self.param)
        es.connect()
        doc = {
            "source_id": str(1231231),
            "source": "tattle-admin",
            "metadata": {},
            "text": "test text to go with the image",
            "image_vec": np.random.randn(512).tolist(),
            "date_added": datetime.utcnow(),
        }
        result = es.store(doc)
        self.assertEqual(result["result"], "created")

    def test_search_vectors(self):
        es = ES(self.param)
        es.connect()
        es.create_index()
        vec = np.random.randn(512).tolist()
        doc = {
            "source_id": str(1231231),
            "source": "tattle-admin",
            "metadata": {"domain": "hate-speech"},
            "text": "test text to go with the image",
            "image_vec": vec,
            "date_added": datetime.utcnow(),
        }

        result = es.store("test_image", doc)
        pp.pprint(result)
        search_result = es.find("test_image", vec)
        es.refresh()
        print("SEARCH RESULTS \n : ")
        pp.pprint(search_result)
        self.assertEqual(result["result"], "created")
        # es.delete_indices()

    def test_store_text(self):
        pass

    def test_search_text(self):
        pass

    def test_store_metadata(self):
        pass

    def test_find_by_metadata_field(self):
        pass

    def delete_indices(self):
        print("DELETING INDICES")
        es = ES(self.param)
        es.connect()
        es.delete_indices()
        print("INDICES DELETED")
        self.assertEqual(1, 1)
