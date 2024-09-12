import logging
from core.models.media import MediaType
from core.config import StoreConfig
from elasticsearch import Elasticsearch, helpers as eshelpers
from .es_vec_mappings import mappings
from .es_vec_adapter import es_to_sanitized
import numpy as np
import inspect
import os
import json

log = logging.getLogger(__name__)


class ES:
    def __init__(self, config: StoreConfig):
        self.es_host = os.environ.get("ES_HOST")
        self.indices = {
            "text": config.parameters.text_index_name,
            "image": config.parameters.image_index_name,
            "video": config.parameters.video_index_name,
            "audio": config.parameters.audio_index_name,
        }

    def connect(self):
        try:
            self.config = {"host": self.es_host, "port": 9200, "scheme": "http"}
            self.client = Elasticsearch(
                [
                    self.config,
                ]
            )
            log.info("Success Connecting to Elasticsearch")
        except Exception:
            log.exception("Error Connecting to Elasticsearch")

    def ping(self):
        return self.client.info()

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
                body = json.loads(mappings[index])
                self.client.indices.create(index=self.indices[index], body=body)
                log.info("{} created".format(self.indices[index]))

    def delete_indices(self):
        for index in self.indices:
            self.client.indices.delete(index=self.indices[index])

    def get_indices(self):
        index_list = ""
        for index in self.indices:
            index_list += self.indices[index] + ","
        index_list = index_list[:-1]
        indices = self.client.indices.get(index=index_list)
        return indices

    def store(self, media_type: MediaType, doc):
        if inspect.isgeneratorfunction(doc):
            bulk_res = eshelpers.bulk(self.client, doc())
            print("----> 6", bulk_res)
            return {"message": "multiple media stored"}
        else:
            result = self.client.index(index=self.indices[media_type.value], body=doc)
            return result

    def refresh(self):
        for index in self.indices:
            self.client.indices.refresh()

    def find(self, index_name, vec):
        if isinstance(vec, np.ndarray):
            vec = vec.tolist()

        calculation = ""
        if index_name == self.indices["text"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'text_vec'))"
        elif index_name == self.indices["image"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'image_vec'))"
        elif index_name == self.indices["video"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'vid_vec'))"
        elif index_name == self.indices["audio"]:
            calculation = "1 / (1 + l2norm(params.query_vector, 'audio_vec'))"

        print("calculation:", calculation)
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

    def find_text(self, text):
        query_body = {
            "size": 10,
            "query": {"bool": {"must": {"match": {"text": text}}}},
        }

        result = self.client.search(index="text", body=query_body)
        res = es_to_sanitized(result)
        return res

    def query(self, fieldName, value):
        query = {
            "bool": {
                # "must": {"match": {"metadata.type": "apple"}},
                "must": {"match": {fieldName: value}},
                # "filter": [{"match_phrase": {"dataset": "asdfasdf-000004"}}],
            }
        }
        result = self.client.search(
            query=query,
            index="text",
            _source=[
                "metadata",
                "dataset",
                "source_id",
                "text",
                "date_added",
                "source",
                "e_kosh_id",
            ],
        )
        res = es_to_sanitized(result)
        return res

    def update(param, doc):
        pass

    # this is an alias for the delete_indices function. i find the name more generic
    def reset(self):
        for index in self.indices:
            self.client.indices.delete(self.indices[index])

    def stats(self):
        indices = self.get_indices()
        return indices
    
    def initialise(self):
        self.optionally_create_index()
