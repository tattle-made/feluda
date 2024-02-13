import unittest
from unittest.case import skip
import requests
import pprint
import os
from elasticsearch import Elasticsearch
from core.operators import audio_vec_embedding
from time import sleep

pp = pprint.PrettyPrinter(indent=4)
'''
Check how many documents have been indexed
curl -X GET "http://es:9200/_cat/indices?v"
Delete all the documents in an index
curl -X POST "http://es:9200/test_audio/_delete_by_query" -H 'Content-Type: application/json' -d'{"query":{"match_all":{}}}'
'''

class TestAudioES(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # ping es server to see if its working
        response = requests.get("http://es:9200")

        if response.status_code == 200:
            print("Elastic search server is running")
        else:
            print("No elasticsearch service found. Tests are bound to fail.")

        cls.es_host = os.environ.get("ES_HOST")
        try:
            cls.config = {"host": cls.es_host, "port": 9200, "scheme": "http"}
            cls.client = Elasticsearch([cls.config,])
            print("Success Connecting to Elasticsearch")
        except Exception:
            print("Error Connecting to Elasticsearch")
    
    @classmethod
    def tearDownClass(cls) -> None:
        print("TEARING DOWN CLASS")
        pass

    def create_test_audio_index(self):
        global index_name
        index_name = "test_audio"
        index_config = {
            "mappings": {
                "_source": {
                    "excludes": ["audio-embedding"]
                },
                "properties": {
                "audio-embedding": {
                    "type": "dense_vector",
                    "dims": 2048,
                    "index": True,
                    "similarity": "cosine"
                },
                }
            }
        }
        try:
            if self.client.indices.exists(index=index_name):
                print(f"Index '{index_name}' already exists.")
                return
            response = self.client.indices.create(index=index_name, body=index_config)
            if response["acknowledged"]:
                print(f"Index '{index_name}' created successfully.")
            else:
                print(f"Failed to create index '{index_name}'.")
        except Exception as e:
            print(f"Error creating index '{index_name}': {e}")
    
    @skip
    def test_store_audio_vector(self):
        # create the audio indice
        self.create_test_audio_index()
        # generate an audio vector
        audio_vec_embedding.initialize(param=None)
        audio_file_path = r'core/operators/sample_data/audio.wav'
        audio_emb = audio_vec_embedding.run(audio_file_path)
        audio_emb_vec = audio_emb.tolist()
        # index the vector
        body = {
            'audio-embedding' : audio_emb_vec,
        }
        result = self.client.index(index=index_name, document=body)
        # print(result)
        self.assertEqual(result["result"], "created")

    # @skip
    def test_search_audio_vector(self):
        # create the audio indice
        self.create_test_audio_index()
        # generate an audio vector
        audio_vec_embedding.initialize(param=None)
        audio_file_path = r'core/operators/sample_data/audio.wav'
        audio_emb = audio_vec_embedding.run(audio_file_path)
        audio_emb_vec = audio_emb.tolist()
        # index the vector
        body = {
            'audio-embedding' : audio_emb_vec,
        }
        self.client.index(index=index_name, document=body)
        # search for it
        query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'audio-embedding') + 1.0",
                        "params": {"query_vector": audio_emb_vec}
                    }
                }
            }
        }
        search_result = self.client.search(index="test_audio", body=query)
        print(search_result)

    @skip
    def test_store_and_search_50files(self):
        self.create_test_audio_index()
        audio_vec_embedding.initialize(param=None)
        audio_folder_path = r'core/operators/sample_data/50_audio_files'
        for file_name in os.listdir(audio_folder_path):
            audio_file_path = os.path.join(audio_folder_path, file_name)
            audio_emb = audio_vec_embedding.run(audio_file_path)
            audio_emb_vec = audio_emb.tolist()
            body = {
                'audio-embedding' : audio_emb_vec,
            }
            self.client.index(index=index_name, document=body)
            sleep(0.5)





    