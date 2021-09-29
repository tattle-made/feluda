from elasticsearch import Elasticsearch
from .es_vec_mappings import mappings
from .es_vec_adapter import es_to_sanitized
import numpy as np


class ES:
    def __init__(self, param):
        self.es_host = param["host_name"]
        self.txt_index_name = param["text_index_name"]
        self.img_index_name = param["image_index_name"]
        self.vid_index_name = param["video_index_name"]
        self.index_types = ["text", "image", "video"]

    def connect(self):
        try:
            self.config = {"host": self.es_host}
            self.client = Elasticsearch(
                [
                    self.config,
                ]
            )
            print("Success Connecting to Elasticsearch")
        except Exception:
            print("Error Connecting to Elasticsearch")

    def create_index(self):
        """
        Checks if an index already exists in Elasticsearch and if not, creates it according to the mapping specified for that index type.
        Note: This uses default shard settings.

        Args:
        es - Elasticsearch client instance
        index - (str) Name of the index
        type - (str) Allowed options are "text", "image" or "video"

        """
        # WARNING: The next line is only for testing index creation and will delete existing indices!
        # es.indices.delete(index=index, ignore=[400,404])

        for index_type in self.index_types:
            if self.client.indices.exists(index=index_type):
                print("Verified that {} exists".format(index_type))
            else:
                print("{} does not exist, creating it now".format(index_type))
                body = mappings[index_type]
                self.client.indices.create(index=index_type, body=body)
                print("{} created".format(index_type))

    def delete_indices(self):
        for index_type in self.index_types:
            self.client.indices.delete(index_type)

    def get_indices(self):
        indices = self.client.indices.get(",".join(self.index_types))
        return indices

    def store(self, doc):

        result = self.client.index(index="image", body=doc)
        return result

    def refresh(self):
        for index_type in self.index_types:
            self.client.indices.refresh(index_type)

    def find(self, index_name, vec):
        if type(vec) == np.ndarray:
            vec = vec.tolist()

        if index_name == "text":
            calculation = "1 / (1 + l2norm(params.query_vector, 'text_vec'))"
        elif index_name == "image":
            calculation = "1 / (1 + l2norm(params.query_vector, 'image_vec'))"
        elif index_name == "video":
            calculation = "1 / (1 + l2norm(params.query_vector, 'vid_vec'))"

        q = {
            "size": 10,  # maximum number of hits returned by the query
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {"source": calculation, "params": {"query_vector": vec}},
                }
            },
        }

        resp = self.client.search(index=index_name, body=q)
        res = es_to_sanitized(resp)
        return res

    def update(param, doc):
        pass

    def delete(id):
        pass


# es_instance = ES()
# es_instance.connect()


# def get_es_instance():
#     return es_instance.client
