from .model import Post
from flask import request
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


class IndexHandler:
    def __init__(self):
        pass

    def index_text(self, operators):
        # post, metadata, config, files, media_type = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)
        # file = request.files["media"]
        # data = json.load(request.files["data"])
        # post = Post.fromRequestData("text", data, file)
        post = Post.fromRequestPayload("text", request)

        # store.save(post)
        # queue.enqueue(post)
        # process(post)

        return {"message": "handle_text"}

    def index_image(self, operators):
        # post = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)

        # text = operators["detect_text_in_image"].run(post)
        # lang = operators["detect_lang_of_text"].run(text)
        # text_vec = operators["text_vec_rep_paraphrase_lxml"].run(text)
        # image_vec = operators["image_vec_rep_resnet"].run(post)
        # composite_vec = operators["combine_vectors_256dim"].run(image_vec, text_vec)
        # repr = composite_vec

        # file = request.files["media"]
        # data = json.load(request.files["data"])
        # post = Post.fromRequestData("image", data, file)
        post = Post.fromRequestPayload("image", request)
        print("TYPE 1 : ", type(post))
        print("TYPE 1 : ", type(post.post_data))

        return {"message": "handle_image"}

    def index_video(self, operators):
        # post, metadata, config, files, media_type = make_post_from_request(req, "text")
        # print(post, metadata, config, files, media_type)

        # file = request.files["media"]
        # data = json.load(request.files["data"])
        # post = Post.fromRequestData("video", data, file)
        post = Post.fromRequestPayload("video", request)
        print("TYPE 1 : ", type(post))
        print("TYPE 1 : ", type(post.post_data))

        return {"message": "handle_video"}

    def enqueue_text(self):

        return {"message": "enqueue_text"}

    def enqueue_image(self):
        return {"message": "enqueue_image"}

    def enqueue_video(self):
        return {"message": "enqueue_video"}

    def represent_text(self, operators):
        post = Post.fromRequestPayload("text", request)
        plain_text = post.post_data.text
        text_vec = operators["text_vec_rep_paraphrase_lxml"].run(post.post_data.text)
        return {"representation": text_vec.tolist(), "plain_text": plain_text}

    def represent_image(self, operators):
        post = Post.fromRequestPayload("image", request)
        image = post.make_from_file(post.file)
        image_vec = operators["image_vec_rep_resnet"].run(image)
        return {"message": "represent_image"}

    def represent_video(self, operators):
        return {"message": "represent_video"}

    def make_handler(self, operators):
        if request.path == "/index/text":
            return self.index_text(operators)
        elif request.path == "/index/image":
            return self.index_image(operators)
        elif request.path == "/index/video":
            return self.index_video(operators)
        elif request.path == "/enqueue/text":
            return self.enqueue_text()
        elif request.path == "/enqueue/image":
            return self.enqueue_image()
        elif request.path == "/enqueue/video":
            return self.enqueue_video()
        elif request.path == "/represent/text":
            return self.represent_text(operators)
        elif request.path == "/represent/image":
            return self.represent_image(operators)
        elif request.path == "/represent/video":
            return self.represent_video(operators)
        else:
            raise "Unsupported Index API endpoint"
