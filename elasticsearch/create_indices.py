import requests, json, os
from elasticsearch import Elasticsearch
from elasticsearch import helpers as eshelpers
import datetime as datetime
import numpy as np

import os, sys, json
from pymongo import MongoClient
from tqdm import tqdm
import datetime

def create_vid_index(host):
    url = 'http://'+host+':9200/vidsearch'
    payload = {
	      "mappings": {
		"properties": {
                  "doc_id" : {
                    "type" : "keyword",
                  },
                  "source" : {
                    "type" : "keyword",
                  },
                  "metadata" : {
                    "type": "object",
                    "enabled" : False
                  },
                  "vec": {
		    "type": "dense_vector",
		    "dims": 512
		  },
                  "is_avg" : {
                      "type" : "boolean",
                  },
                  "duration" : {
                    "type" : "float"
                  },
                  "n_keyframes" : {
                    "type" : "short"
                  }
		}
	      }
	    }
    res = requests.put(url, json = payload)
    if res.status_code != 200:
        print(res.content)
    return res

def create_txt_index(host):
    url = 'http://'+host+':9200/txtsearch'
    payload = {
              "mappings": {
        	"properties": {
        	  "doc_id" : {
                    "type" : "keyword",
                  },
                  "source" : {
                    "type" : "keyword",
                  },
                  "metadata" : {
                    "type": "object",
                    "enabled" : False
                  },
		  "vec": {
		    "type": "dense_vector",
		    "dims": 300
		  },
                  "text" : {
                    "type" : "text"
                  }
        	}
              }
            }
    res = requests.put(url, json = payload)
    if res.status_code != 200:
        print(res.content)
    return res
 
def create_img_index(host):
    url = 'http://'+host+':9200/imgsearch'
    payload = {
	      "mappings": {
		"properties": {
                  "doc_id" : {
                    "type" : "keyword",
                  },
                  "source" : {
                    "type" : "keyword",
                  },
                  "metadata" : {
                    "type": "object",
                    "enabled" : False
                  },
		  "vec": {
		    "type": "dense_vector",
		    "dims": 512
		  },
		}
	      }
	    }
    res = requests.put(url, json = payload)
    if res.status_code != 200:
        print(res.content)
    return res

if __name__ == "__main__":
    host = os.environ['ES_HOST']
    create_vid_index(host)
    create_img_index(host)
    create_txt_index(host)
