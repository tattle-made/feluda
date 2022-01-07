from dataclasses import dataclass
from core.models.media import MediaType
from core.models.media_factory import media_factory
from flask import request
import json
from core.feluda import Feluda
import logging

log = logging.getLogger(__name__)


class SearchRequestModel:
    pass


class SearchHandler:
    def __init__(self, feluda: Feluda):
        self.feluda = feluda

    def handle_search(self):
        print("---> 1")
        try:
            if request.content_type == "application/json":
                payload = request.get_json()
                if payload["query_type"] == "text":
                    results = self.feluda.store.find_text(payload["text"])
                    return {"matches": results}
                elif payload["query_type"] == "raw_query":
                    return "Method Unimplemented", 501
                else:
                    return {"message": "Unsupported Query Type"}, 400
            elif request.content_type == "multipart/form-data":
                print("---> 1")
                data = json.load(request.files["data"])
                print("---> 2", data)
                if data["query_type"] == "image":
                    file = request.files["media"]
                    print(file, type(file))
                    image_obj = media_factory[MediaType.IMAGE].make_from_file_in_memory(
                        file
                    )
                    image_vec = self.feluda.operators.active_operators[
                        "image_vec_rep_resnet"
                    ].run(image_obj)
                    results = self.feluda.store.find("image", image_vec)
                    return {"matches": results}
                elif data["query_type"] == "video":
                    file = request.files["media"]
                    print(file, type(file))
                    vid_obj = media_factory[MediaType.VIDEO].make_from_file_in_memory(
                        file
                    )
                    vid_vec = self.feluda.operators.active_operators[
                        "vid_vec_rep_resnet"
                    ].run(vid_obj)
                    average_vector = next(vid_vec)
                    results = self.feluda.store.find("image", average_vector)
                    return {"matches": []}
                else:
                    return {"message": "Unsupported Query Type"}
            else:
                return "Unable to handle Index Request", 400
        except:
            log.exception("Unable to handle Index Request")
            return "Unable to handle Index Request", 400

    def make_handlers(self):
        print(request.path)
        if request.path == "/search":
            return self.handle_search()
        else:
            raise "Unsupported Health API endpoint"


class SearchEndpoint:
    def __init__(self, feluda: Feluda):
        self.feluda = feluda

    def get_routes(self):
        return [("/search", "search", ["POST"])]

    def get_handler(self):
        handler = SearchHandler(self.feluda)
        return handler.make_handlers()
