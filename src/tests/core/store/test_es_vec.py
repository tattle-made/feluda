import unittest
from unittest.case import skip
import requests
from requests.exceptions import ConnectTimeout
from core.store.es_vec import ES
from core.config import StoreConfig, StoreEntity, StoreESParameters
from core.models.media import MediaType
import pprint
from datetime import datetime
import numpy as np
from time import sleep

pp = pprint.PrettyPrinter(indent=4)


class TestES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            print("-----------------ES TEST---------------------")
            # ping es server to see if its working
            response = requests.get("http://es:9200", timeout=(3.05, 5))

            if response.status_code == 200:
                print("Elastic search server is running")
            else:
                print("No elasticsearch service found. Tests are bound to fail.")
            param_dict = {
                "host_name": "es",
                "text_index_name": "test_text",
                "image_index_name": "test_image",
                "video_index_name": "test_video",
                "audio_index_name": "test_audio",
            }
            cls.param = StoreConfig(
                entities=[
                    StoreEntity(
                        label="test",
                        type="es",
                        parameters=StoreESParameters(
                            host_name=param_dict["host_name"],
                            image_index_name=param_dict["image_index_name"],
                            text_index_name=param_dict["text_index_name"],
                            video_index_name=param_dict["video_index_name"],
                            audio_index_name=param_dict["audio_index_name"],
                        ),
                    )
                ]
            )
        except ConnectTimeout:
            print('Request has timed out')

    @classmethod
    def tearDownClass(cls) -> None:
        print("TEARING DOWN CLASS")
        pass

    # def tearDown(self) -> None:
    #     pass

    # @skip
    def test_create_indices(self):
        print(self.param.entities[0])
        es = ES(self.param.entities[0])
        es.connect()
        es.optionally_create_index()
        indices = es.get_indices()
        # print(indices)

        self.assertEqual(
            indices["test_text"]["mappings"]["properties"]["text"]["analyzer"],
            "standard",
        )
        self.assertEqual(
            indices["test_image"]["mappings"]["properties"]["image_vec"]["dims"], 512
        )
        self.assertEqual(
            indices["test_video"]["mappings"]["properties"]["vid_vec"]["dims"], 512
        )
        self.assertEqual(
            indices["test_audio"]["mappings"]["properties"]["audio_vec"]["dims"], 512
        )

    @skip
    def test_store_image(self):
        es = ES(self.param)
        es.connect()
        doc = {
            "e_kosh_id": str(1231231),
            "dataset": "test-dataset-id",
            "source": "tattle-admin",
            "metadata": {},
            "text": "test text to go with the image",
            "image_vec": np.random.randn(512).tolist(),
            "date_added": datetime.utcnow(),
        }
        mediaType = MediaType.IMAGE
        result = es.store(mediaType, doc)
        self.assertEqual(result["result"], "created")

    # @skip
    def test_store_and_search_vectors(self):
        es = ES(self.param.entities[0])
        es.connect()
        es.optionally_create_index()
        vec = np.random.randn(512).tolist()
        doc = {
            "e_kosh_id": str(1231231),
            "dataset": "test-dataset-id",
            "source": "tattle-admin",
            "metadata": {"domain": "hate-speech"},
            "text": "test text to go with the image",
            "image_vec": vec,
            "date_added": datetime.utcnow(),
        }
        es.store(MediaType.IMAGE, doc)
        # pp.pprint(result)
        sleep(2)
        search_result = es.find("test_image", vec)
        es.refresh()
        print("SEARCH RESULTS \n : ")
        print(search_result)
        self.assertEqual(search_result[0]["dataset"], "test-dataset-id")
        es.delete_indices()

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
        es = ES(self.param.entities[0])
        es.connect()
        es.delete_indices()
        print("INDICES DELETED")
        self.assertEqual(1, 1)
