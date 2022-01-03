import logging
from api.core.models.media import MediaType
from core.config import StoreConfig

log = logging.getLogger(__name__)
from elasticsearch import Elasticsearch, helpers as eshelpers
from .es_vec_mappings import mappings
from .es_vec_adapter import es_to_sanitized
import numpy as np
import inspect


class ES:
    def __init__(self, config: StoreConfig):
        self.es_host = config.parameters.host_name
        self.indices = {
            "text": config.parameters.text_index_name,
            "image": config.parameters.image_index_name,
            "video": config.parameters.video_index_name,
        }

    def connect(self):
        try:
            self.config = {"host": self.es_host}
            self.client = Elasticsearch(
                [
                    self.config,
                ]
            )
            log.info("Success Connecting to Elasticsearch")
        except Exception:
            log.exception("Error Connecting to Elasticsearch")

    def optionally_create_index(self):
        """
        Checks if an index already exists in Elasticsearch and if not, creates it according to the mapping specified for that index type.
        Note: This uses default shard settings.

        Args:
        es - Elasticsearch client instance
        index - (str) Name of the index
        type - (str) Allowed options are "text", "image" or "video"
        """
        for index in self.indices:
            if self.client.indices.exists(index=self.indices[index]):
                log.info("Verified that {} exists".format(self.indices[index]))
            else:
                log.info(
                    "{} does not exist, creating it now".format(self.indices[index])
                )
                body = mappings[index]
                self.client.indices.create(index=self.indices[index], body=body)
                log.info("{} created".format(self.indices[index]))

    def delete_indices(self):
        for index in self.indices:
            self.client.indices.delete(self.indices[index])

    def get_indices(self):
        index_list = ""
        for index in self.indices:
            index_list += self.indices[index] + ","
        index_list = index_list[:-1]
        indices = self.client.indices.get(index_list)
        return indices

    def store(self, media_type: MediaType, doc):
        if inspect.isgenerator(doc):
            bulk_res = eshelpers.bulk(self.client, doc)
            return bulk_res
        else:
            result = self.client.index(index=self.indices[media_type.value], body=doc)
            return result

    def refresh(self):
        for index in self.indices:
            self.client.indices.refresh(self.indices[index])

    def find(self, index_name, vec):
        if type(vec) == np.ndarray:
            vec = vec.tolist()

        if index_name == self.indices["text"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'text_vec'))"
        elif index_name == self.indices["image"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'image_vec'))"
        elif index_name == self.indices["video"]:
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
