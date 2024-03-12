import unittest
from unittest.case import skip
import requests
from requests.exceptions import ConnectTimeout
from core.store.es_vec import ES
from core.config import StoreConfig, StoreParameters
from core.models.media import MediaType
from core.models.media_factory import AudioFactory
import pprint
from datetime import datetime
from core.operators import audio_vec_embedding
from time import sleep
import os

pp = pprint.PrettyPrinter(indent=4)
"""
Check how many documents have been indexed
curl -X GET "http://es:9200/_cat/indices?v"
Delete all the documents in an index
curl -X POST "http://es:9200/test_audio/_delete_by_query" -H 'Content-Type: application/json' -d'{"query":{"match_all":{}}}'
Delete the indice
curl -X DELETE "http://es:9200/test_audio"
Refresh the indice
curl -X POST "http://es:9200/test_audio/_refresh"
"""


class TestAudioES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
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
                label="test",
                type="es",
                parameters=StoreParameters(
                    host_name=param_dict["host_name"],
                    image_index_name=param_dict["image_index_name"],
                    text_index_name=param_dict["text_index_name"],
                    video_index_name=param_dict["video_index_name"],
                    audio_index_name=param_dict["audio_index_name"],
                ),
            )
        except ConnectTimeout:
            print('Request has timed out')

    @classmethod
    def tearDownClass(cls) -> None:
        print("TEARING DOWN CLASS")
        pass

    def test_create_audio_indice(self):
        es = ES(self.param)
        es.connect()
        es.optionally_create_index()
        indices = es.get_indices()
        self.assertEqual(
            indices["test_audio"]["mappings"]["properties"]["audio_vec"]["dims"], 2048
        )

    @skip
    def test_store_audio(self):
        es = ES(self.param)
        es.connect()
        audio_vec_embedding.initialize(param=None)
        audio_file_path = r"core/operators/sample_data/audio.wav"
        audio_emb = audio_vec_embedding.run(audio_file_path)
        audio_emb_vec = audio_emb.tolist()
        doc = {
            "e_kosh_id": str(1231231),
            "dataset": "test-dataset-id",
            "metadata": {},
            "audio_vec": audio_emb_vec,
            "date_added": datetime.utcnow(),
        }
        mediaType = MediaType.AUDIO
        result = es.store(mediaType, doc)
        # print(result)
        self.assertEqual(result["result"], "created")

    @skip
    def test_store_and_search_audio(self):
        es = ES(self.param)
        es.connect()
        audio_vec_embedding.initialize(param=None)
        audio_file_path = AudioFactory.make_from_file_on_disk(
            r"core/operators/sample_data/audio.wav"
        )
        audio_emb = audio_vec_embedding.run(audio_file_path)
        audio_emb_vec = audio_emb.tolist()
        doc = {
            "e_kosh_id": str(1233333333),
            "dataset": "test-dataset-id",
            "metadata": {},
            "audio_vec": audio_emb_vec,
            "date_added": datetime.utcnow(),
        }
        mediaType = MediaType.AUDIO
        es.store(mediaType, doc)
        sleep(4)
        search_result = es.find("test_audio", audio_emb_vec)
        print(search_result)
        self.assertEqual(search_result[0]["dataset"], "test-dataset-id")
        es.delete_indices()

    @skip
    def test_store_and_search_50files(self):
        es = ES(self.param)
        es.connect()
        mediaType = MediaType.AUDIO
        audio_vec_embedding.initialize(param=None)
        audio_folder_path = r"core/operators/sample_data/50_audio_files"
        count = 1
        # store 50 files
        for file_name in os.listdir(audio_folder_path):
            audio_file_path = os.path.join(audio_folder_path, file_name)
            # generate an audio vector
            audio_emb = audio_vec_embedding.run(audio_file_path)
            audio_emb_vec = audio_emb.tolist()
            doc = {
                "e_kosh_id": str(count),
                "dataset": "test-dataset-id",
                "metadata": {},
                "audio_vec": audio_emb_vec,
                "date_added": datetime.utcnow(),
            }
            es.store(mediaType, doc)
            print(f"----------{count}---------------")
            count = count + 1
        print(f"Indexed {count} files")
        sleep(3)
        audio_to_search = (
            r"core/operators/sample_data/100_audio_files/a-cappella-chorus.wav"
        )
        audio_to_search_emb = audio_vec_embedding.run(audio_to_search)
        audio_to_search_emb_vec = audio_to_search_emb.tolist()
        search_result = es.find("test_audio", audio_to_search_emb_vec)
        print(search_result)
        self.assertEqual(search_result[0]["dataset"], "test-dataset-id")
