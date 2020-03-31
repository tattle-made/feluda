import requests, json, os
from elasticsearch import Elasticsearch
from elasticsearch import helpers as eshelpers
import numpy as np

def create_index():
    url = "http://localhost:9200/test2"
    payload = {
	      "mappings": {
		"properties": {
		  "image_vector": {
		    "type": "dense_vector",
		    "dims": 512
		  }
		}
	      }
	    }
    res = requests.put(url, json = payload)
    return res

def upload_dummy_data():
    es = Elasticsearch()
    n_docs = 100
    data = {i:np.random.randn(512).tolist() for i in range(n_docs)}
    def gendata():
        for k, v in data.items():
            yield {
                "_index": "test2",
                "_id": k,
                "image_vector" : v}

    res = eshelpers.bulk(es, gendata())
    return res

def query(vec):
    #url = "127.0.0.1"
    #config = {'host' : url}
    es = Elasticsearch()
    q = {
	"size": 2,
        "query": {
	    "script_score": {
	      "query" : {
		"match_all" : {}
	      },
	      "script": {
		"source": "1 / (1 + l2norm(params.query_vector, 'image_vector'))", 
		"params": {
		  "query_vector": vec
		}
	      }
	    }
	  }
        }

    resp = es.search(index="test2", body = q)
    print(resp)

if __name__ == "__main__":
    create_index()
    upload_dummy_data()
    vec = np.random.randn(512).tolist()
    query(vec)

