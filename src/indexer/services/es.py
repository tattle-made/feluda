from elasticsearch import Elasticsearch
import os 
from dotenv import load_dotenv
load_dotenv()
import logging

class ES():
    def __init__(self):
        self.es_host = os.environ.get('ES_HOST')

    def connect(self):
        try:
            self.config = {'host': self.es_host}
            self.client = Elasticsearch([self.config,])
            print('Success Connecting to Elasticsearch')
        except Exception:
            print('Error Connecting to Elasticsearch')
            print(logging.traceback.format_exc())

es_instance = ES()
es_instance.connect()

def get_es_instance():
    return es_instance.client