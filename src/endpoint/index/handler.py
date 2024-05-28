# from pydoc import plain
# from typing import Callable
from core.models.media import MediaType  # MediaMode,
from core.feluda import Feluda

# from core.store.es_vec_adapter import text_rep_to_es_doc
from .model import ConfigMode, Post
from flask import request

# import json
from typing import Callable
import logging

# import inspect
from datetime import datetime

log = logging.getLogger(__name__)


def generateRepresentation(post: Post, operators):
    file = post.getMedia()
    if post.type == MediaType.TEXT:
        plain_text = file["text"]
        # lang = operators["detect_lang_of_text"].run(plain_text)
        lang = "en"
        entities = operators["ner_extraction"].run(plain_text)
        return {"plain_text": plain_text, "lang": lang, "entities": entities}
    elif post.type == MediaType.IMAGE:
        image_vec = operators["image_vec_rep_resnet"].run(file)
        # text = operators["detect_text_in_image"].run(file)
        # entities = operators["ner_extraction"].run(text["text"])
        return {
            "vector_representation": image_vec,
            # "text": text["text"],
            # "entities": entities,
        }
    elif post.type == MediaType.VIDEO:
        video_vector_generator = operators["vid_vec_rep_resnet"].run(file)
        return video_vector_generator


def generateDocument(post: Post, representation: any):
    base_doc = {
        "e_kosh_id": str(post.post_data.id),
        "dataset": str(post.post_data.datasource_id),
        "metadata": post.metadata,
        "date_added": datetime.now().isoformat(),
    }
    if post.type == MediaType.TEXT:
        base_doc["text"] = representation["plain_text"]
        base_doc["lang"] = representation["lang"]
        base_doc["suggestion"] = representation["entities"]
        return base_doc
    elif post.type == MediaType.IMAGE:
        base_doc["image_vec"] = representation["vector_representation"]
        # base_doc["text"] = representation["text"]
        # base_doc["suggestion"] = representation["entities"]
        return base_doc
    elif post.type == MediaType.VIDEO:

        def generatorDoc():
            for vector in representation:
                base_doc["_index"] = "video"
                base_doc["vid_vec"] = vector["vid_vec"]
                base_doc["is_avg"] = vector["is_avg"]
                base_doc["duration"] = vector["duration"]
                base_doc["n_keyframes"] = vector["n_keyframes"]
                yield base_doc

        return generatorDoc


class IndexHandler:
    def __init__(self, feluda: Feluda):
        self.feluda = feluda

    def index(self, generateRepresentation: Callable):
        try:
            if request.content_type == "application/json":
                post = Post.fromRequestPayloadJSON(request.get_json())
            elif request.content_type == "multipart/form-data":
                post = Post.fromRequestPayload(request)
            else:
                return "Unable to handle Index Request", 400

            config_mode = post.config.mode

            if config_mode == ConfigMode.ENQUEUE:
                self.feluda.queue.message(
                    "tattle-search-index-queue", request.get_json()
                )
                return {"message": "Post Indexed"}
            elif config_mode == ConfigMode.STORE:
                operators = self.feluda.operators.active_operators
                representation = generateRepresentation(post, operators)
                document = generateDocument(post, representation)
                save_result = self.feluda.store["es_vec"].store(post.type, document)
                return {"message": "ok", "data": save_result.get("_id", "default")}
            elif config_mode == ConfigMode.REFLECT:
                return "Method Unimplemented", 501
            else:
                return "Unexpected Index Mode", 400

        except Exception as e:
            log.exception("Unable to handle Index Request:", e)
            return "Unable to handle Index Request", 400

    def make_handler(self):
        if request.path == "/index":
            return self.index(generateRepresentation)
            # return self.test_endpoint()
