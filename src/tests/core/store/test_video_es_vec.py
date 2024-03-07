import unittest

# from unittest.case import skip
import pprint
from core.store.es_vec import ES
from core.config import StoreConfig, StoreParameters
from core.models.media import MediaType
from core.models.media_factory import VideoFactory
from core.operators import vid_vec_rep_resnet
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)
"""
# Get indexing stats
curl -X GET "http://es:9200/_stats/indexing?pretty"
# Check how many documents have been indexed
curl -X GET "http://es:9200/_cat/indices?v"
# Delete all the documents in an index
curl -X POST "http://es:9200/video/_delete_by_query" -H 'Content-Type: application/json' -d'{"query":{"match_all":{}}}'
"""


class TestVideoES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        param_dict = {
            "host_name": "es",
            "text_index_name": "text",
            "image_index_name": "image",
            "video_index_name": "video",
            "audio_index_name": "audio",
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

    @classmethod
    def tearDownClass(cls) -> None:
        print("TEARING DOWN CLASS")

    @staticmethod
    def generate_document(post_id: str, representation: any):
        base_doc = {
            "e_kosh_id": "",
            "dataset": post_id,
            "metadata": None,
            "date_added": datetime.now().isoformat(),
        }

        def generator_doc():
            for vector in representation:
                base_doc["_index"] = "video"
                base_doc["vid_vec"] = vector["vid_vec"]
                base_doc["is_avg"] = vector["is_avg"]
                base_doc["duration"] = vector["duration"]
                base_doc["n_keyframes"] = vector["n_keyframes"]
                yield base_doc

        return generator_doc

    # @skip
    def test_1_store_video_vector(self):
        es = ES(self.param)
        es.connect()

        # generate video embedding
        vid_vec_rep_resnet.initialize(param=None)
        file_name = "sample-cat-video.mp4"
        video_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4"
        video = VideoFactory.make_from_url(video_url)
        embedding = vid_vec_rep_resnet.run(video)
        doc = self.generate_document(file_name, embedding)

        media_type = MediaType.VIDEO
        result = es.store(media_type, doc)
        print("result:", result)

        self.assertEqual(result["message"], "multiple media stored")

    # @skip
    def test_2_search_video_vector(self):
        es = ES(self.param)
        es.connect()
        es.optionally_create_index()

        # generate video embedding
        vid_vec_rep_resnet.initialize(param=None)
        file_name = "sample-cat-video.mp4"
        video_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4"
        video = VideoFactory.make_from_url(video_url)
        embedding = vid_vec_rep_resnet.run(video)
        average_vector = next(embedding)
        search_result = es.find("video", average_vector.get("vid_vec"))
        print("SEARCH RESULTS \n : ")
        pp.pprint(search_result)
        file_found = False
        for result in search_result:
            if result.get("dataset") == file_name:
                file_found = True
                break
        self.assertTrue(file_found, f"File {file_name} not found in any search result.")
