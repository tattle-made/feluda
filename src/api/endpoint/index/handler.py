from typing import Callable
from core.models.media import MediaMode, MediaType
from core.feluda import Feluda
from core.store.es_vec_adapter import text_rep_to_es_doc
from .model import ConfigMode, Post, Config, ImageFactory
from flask import request
import json
from typing import Callable
import logging
import inspect

log = logging.getLogger(__name__)


def generateRepresentation(post: Post, operators):
    file = post.getMedia()
    if post.type == MediaType.TEXT:
        plain_text = file["text"]
        text_vec = operators["text_vec_rep_paraphrase_lxml"].run(plain_text)
        return {"plain_text": plain_text, "vector_representation": text_vec.tolist()}
    elif post.type == MediaType.IMAGE:
        image_vec = operators["image_vec_rep_resnet"].run(file)
        return {"vector_representation": image_vec.tolist()}
    elif post.type == MediaType.VIDEO:
        video_vector_generator = operators["vid_vec_rep_resnet"].run(file)
        return video_vector_generator


class IndexHandler:
    def __init__(self, feluda: Feluda):
        self.feluda = feluda

    def index(self, generateRepresentation: Callable):
        response = {}
        print(type(response))

        try:
            post = Post.fromRequestPayload(request)
        except Exception as e:
            log.exception("Malformed Index Payload.")
            response = {
                "error": "The Index Payload seems malformed. Please refer to documentation at /reference"
            }
            return response

        config_mode = post.config.mode
        print(config_mode)

        if config_mode == ConfigMode.ENQUEUE:
            # add request to queue
            pass
        elif config_mode == ConfigMode.STORE:
            operators = self.feluda.operators.active_operators
            representation = generateRepresentation(post, operators)
            response = {"message": "post stored"}
            if inspect.isgenerator(representation) == True:
                # representation is inside a generator
                print("its a generator")
                pass
            else:
                # representation is an object that can be saved
                pass
            # store in es or return right away
        elif config_mode == ConfigMode.REFLECT:
            pass
        else:
            pass

        return response

    def make_handler(self):
        if request.path == "/index":
            return self.index(generateRepresentation)
