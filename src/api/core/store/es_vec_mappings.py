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
                        "text": {
                            "type": "text",
                            "analyzer": "standard"
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
