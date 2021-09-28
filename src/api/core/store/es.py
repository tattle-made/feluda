from elasticsearch import Elasticsearch

mappings = {
    "text": """{
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
                            "dims": 768
                        },
                        "date_added": {
                            "type": "date"
                        }
                    }
                }
            }""",
    "image": """{
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
                        "image_vec": {
                            "type":"dense_vector",
                            "dims": 512
                        },
                        "date_added": {
                            "type": "date"
                        }
                    }
                }
            }""",
    "video": """{
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
            }""",
}


class ES:
    def __init__(self, param):
        self.es_host = os.environ.get("ES_HOST")
        self.vid_index = os.environ["ES_VID_INDEX"]
        self.img_index = os.environ["ES_IMG_INDEX"]
        self.txt_index = os.environ["ES_TXT_INDEX"]
        self.connect()
        self.create_index(es, es_vid_index, index_type="video")
        self.create_index(es, es_img_index, index_type="image")
        self.create_index(es, es_txt_index, index_type="text")

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

    def create_index(self, index, index_type):
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

        if self.client.indices.exists(index=index):
            print("Verified that {} exists".format(index))
        else:
            print("{} does not exist, creating it now".format(index))
            body = mappings[index_type]
            self.client.indices.create(index=index, body=body)
            print("{} created".format(index))

    def store(doc):
        pass

    def update(param, doc):
        pass

    def delete(id):
        pass

    def find(query):
        pass


# es_instance = ES()
# es_instance.connect()


# def get_es_instance():
#     return es_instance.client
