from .model import make_post_from_request
from flask import request
import json


class IndexHandler:
    def __init__(self):
        pass

    def handle_text(self, operators):
        # post, metadata, config, files, media_type = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)
        print("---")
        print(request.get_json())
        print(type(request.files["media"]))
        print(json.load(request.files["data"]))
        print("---")

        return {"message": "handle_text"}

    def handle_image(self, operators):
        # post = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)

        # text = operators["detect_text_in_image"].run(post)
        # lang = operators["detect_lang_of_text"].run(text)
        # text_vec = operators["text_vec_rep_paraphrase_lxml"].run(text)
        # image_vec = operators["image_vec_rep_resnet"].run(post)
        # composite_vec = operators["combine_vectors_256dim"].run(image_vec, text_vec)
        # repr = composite_vec

        return {"message": "handle_image"}

    def handle_video(self, operators):
        # post, metadata, config, files, media_type = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)
        return {"message": "handle_video"}

    def make_handler(self, operators):
        if request.path == "/index/text":
            return self.handle_text(operators)
        elif request.path == "/index/image":
            return self.handle_image(operators)
        elif request.path == "/index/video":
            return self.handle_video(operators)
        else:
            raise "Unsupported Index API endpoint"
