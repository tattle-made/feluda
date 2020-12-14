from elasticsearch import Elasticsearch
from datetime import datetime

def check_index(es, index, index_type):

    """
    Checks if an index already exists in Elasticsearch and if not, creates it according to the mapping specified for that index type.
    Note: This uses default shard settings.

    Args:
    es - Elasticsearch client instance
    index - (str) Name of the index 
    type - (str) Allowed options are "text", "image" or "video"

    """
    # The next line is only for testing index creation AND SHOULD BE REMOVED
    # es.indices.delete(index=index, ignore=[400,404])

    if es.indices.exists(index=index):
        print("Verified that {} exists".format(index))
    else:
        print("{} does not exist, creating it now".format(index))
        body = get_mapping(index_type)
        es.indices.create(index=index, body=body)
        print("{} created".format(index))
        

def get_mapping(index_type):

    mappings = {
        "text": '''{
                "mappings": {
                    "properties":{
                        "source_id": {
                            "type": "keyword"
                        },
                        "source": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "text": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "lang": {
                            "type": "keyword"
                        },
                        "text_vec": {
                            "type":"dense_vector",
                            "dims": 300
                        },
                        "date_added": {
                            "type": "date"
                        }
                    }
                }
            }''',
        "image": '''{
                "mappings": {
                    "properties":{
                        "source_id": {
                            "type": "keyword"
                        },
                        "source": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "has_text": {
                            "type": "boolean"
                        },
                        "text": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "text_vec": {
                            "type":"dense_vector",
                            "dims": 300
                        },
                        "lang": {
                            "type": "keyword"
                        },
                        "image_vec": {
                            "type":"dense_vector",
                            "dims": 512
                        },
                        "combined_vec": {
                            "type":"dense_vector",
                            "dims": 812
                        },
                        "date_added": {
                            "type": "date"
                        }
                    }
                }
            }''', 
        "video": '''{
                "mappings": {
                    "properties":{
                        "source_id": {
                            "type": "keyword"
                        },
                        "source": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "vid_vec": {
                            "type":"dense_vector",
                            "dims": 512
                        },
                        "date_added": {
                            "type": "date"
                        },
                        "is_avg": {
                            "type": "boolean"
                        },
                        "duration": {
                            "type": "float"
                        },
                        "n_keyframes": {
                            "type": "integer"
                        }
                    }
                }
            }'''
    }

    return mappings[index_type]