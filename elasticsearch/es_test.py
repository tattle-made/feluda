import requests, json, os
from elasticsearch import Elasticsearch
from elasticsearch import helpers as eshelpers
import datetime as datetime
import numpy as np

import os, sys, json
from pymongo import MongoClient
from tqdm import tqdm
import datetime

def create_index(host, index):
    url = 'http://'+host+':9200/'+index
    #payload = {
    #          "mappings": {
    #    	"properties": {
    #    	  "image_vector": {
    #    	    "type": "dense_vector",
    #    	    "dims": 512
    #    	  },
    #              "text_vector" : {
    #                "type" : "dense_vector",
    #                "dims" : 300,
    #              },
    #              "text" : {
    #                "type" : "text"
    #              }
    #    	}
    #          }
    #        }
    payload = {
	      "mappings": {
		"properties": {
		  "image_vector": {
		    "type": "dense_vector",
		    "dims": 512
		  },
		}
	      }
	    }
 
    res = requests.put(url, json = payload)
    return res

def upload_dummy_data(host, index):
    config = {'host': host}
    es = Elasticsearch([config,])
    n_docs = 100
    data = {i:np.random.randn(512).tolist() for i in range(n_docs)}
    def gendata():
        for k, v in data.items():
            yield {
                "_index": index,
                "_id": k,
                "image_vector" : v}

    res = eshelpers.bulk(es, gendata())

    def gendata2():
        yield{
                "_index" : index,
                "_id" : 101
        }
    res = eshelpers.bulk(es, gendata2())
    return res

def upload_data(host, index):
    config = {'host': host}
    es = Elasticsearch([config,])
    data = json.loads(open('data.json').read())
    def gendata():
        for k, v in data.items():
            yield {
                "_index": index,
                "_id": k,
                "image_vector" : v}

    res = eshelpers.bulk(es, gendata())

def upload_mongo_data(host, index):
    config = {'host': host}
    es = Elasticsearch([config,])
    mongo_url = os.environ['MONGO_URL']
    cli = MongoClient(mongo_url)
    db = cli.documents
    cur = db.docs.find().limit(100)
    def gendata():
        for doc in cur:
            #if 'image_vec' not in doc or 'text_vec' not in doc or 'text' not in doc:
            #    continue
            yield {
                '_id' : doc['doc_id'],
                'image_vector' : doc.get('image_vec')
                    'image_vector' : doc.get('image_vec'),
                    'text_vector'  : doc.get('text_vec'),
            }

    res = eshelpers.bulk(es, gendata())
    return res
    cli.close()

def query(host, index, vec):
    config = {'host': host}
    es = Elasticsearch([config,])
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

    resp = es.search(index=index, body = q)
    print(resp)

if __name__ == "__main__":
    host = os.environ['ES_HOST']
    index = os.environ['ES_INDEX']
    create_index(host, index)
    upload_data(host, index)
    #query(vec)
