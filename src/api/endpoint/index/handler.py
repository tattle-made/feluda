from typing import Callable
from core.models.media import MediaMode, MediaType
from core.feluda import Feluda
from core.store.es_vec_adapter import text_rep_to_es_doc
from .model import ConfigMode, Post
from flask import request
import json
from typing import Callable
import logging
import inspect
from datetime import datetime

log = logging.getLogger(__name__)


def generateRepresentation(post: Post, operators):
    file = post.getMedia()
    if post.type == MediaType.TEXT:
        plain_text = file["text"]
        return {"plain_text": plain_text}
    elif post.type == MediaType.IMAGE:
        image_vec = operators["image_vec_rep_resnet"].run(file)
        return {"vector_representation": image_vec}
    elif post.type == MediaType.VIDEO:
        video_vector_generator = operators["vid_vec_rep_resnet"].run(file)
        return video_vector_generator


def generateDocument(post: Post, representation: any):
    base_doc = {
        "source_id": str(post.post_data.id),
        "dataset": str(post.post_data.datasource_id),
        "metadata": post.metadata,
        "date_added": datetime.utcnow().strftime("%d%m%Y"),
    }
    if post.type == MediaType.TEXT:
        base_doc["text"] = representation["plain_text"]
        base_doc["lang"] = "en"
        return base_doc
    elif post.type == MediaType.IMAGE:
        base_doc["image_vec"] = representation["vector_representation"]
        base_doc["text"] = "image text"
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
        response = {}

        # fix : not sure why request.files can be accessed only once.
        data = json.load(request.files["data"])
        file = request.files.get("media", None)

        try:
            post = Post.fromRequestPayload(data, file)
        except Exception as e:
            log.exception("Malformed Index Payload.")
            response = {
                "error": "The Index Payload seems malformed. Please refer to documentation at /reference"
            }
            return response

        config_mode = post.config.mode

        if config_mode == ConfigMode.ENQUEUE:
            self.feluda.queue.message("tattle-search-index-queue", data)
            return {"msg": "done"}
        elif config_mode == ConfigMode.STORE:
            operators = self.feluda.operators.active_operators
            representation = generateRepresentation(post, operators)
            document = generateDocument(post, representation)
            save_result = self.feluda.store.store(post.type, document)
            return save_result
        elif config_mode == ConfigMode.REFLECT:
            pass
        else:
            pass

        return response

    def make_handler(self):
        if request.path == "/index":
            return self.index(generateRepresentation)
