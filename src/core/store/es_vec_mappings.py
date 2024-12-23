mappings = {
    "text": """{
                "mappings": {
                    "properties":{
                        "e_kosh_id": {
                            "type": "keyword"
                        },
                        "dataset": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "text": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "text_vec": {
                            "type":"dense_vector",
                            "dims": 768
                        },
                        "suggestion": {
                            "type" : "completion"
                        },
                        "lang": {
                            "type": "keyword"
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
                        "e_kosh_id": {
                            "type": "keyword"
                        },
                        "dataset": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "image_vec": {
                            "type":"dense_vector",
                            "dims": 512
                        },
                        "text": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "suggestion": {
                            "type" : "completion"
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
                        "e_kosh_id": {
                            "type": "keyword"
                        },
                        "dataset": {
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
    "audio": """{
                "mappings": {
                    "properties":{
                        "e_kosh_id": {
                            "type": "keyword"
                        },
                        "dataset": {
                            "type": "keyword"
                        },
                        "metadata": {
                            "type": "object"
                        },
                        "audio_vec": {
                            "type":"dense_vector",
                            "dims": 512
                        },
                        "date_added": {
                            "type": "date"
                        }
                    }
                }
            }""",
}
