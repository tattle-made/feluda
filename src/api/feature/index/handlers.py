from .model import make_post_from_request
from dataclasses import dataclass


def handle_text(req, operators):
    post, metadata, config, files, media_type = make_post_from_request(req, "text")
    print(post, metadata, config, files, media_type)

    def handle():
        pass

    return handle


def handle_image(req, operators):
    post = make_post_from_request(req, "text")
    # print(post, metadata, config, files, media_type)

    def handle():
        text = operators["detect_text_in_image"].run(post)
        lang = operators["detect_lang_of_text"].run(text)
        # text_vec = operators["text_vec_rep_paraphrase_lxml"].run(text)
        image_vec = operators["image_vec_rep_resnet"].run(post)
        # composite_vec = operators["combine_vectors_256dim"].run(image_vec, text_vec)
        # repr = composite_vec

    return handle


def handle_video(req, operators):
    post, metadata, config, files, media_type = make_post_from_request(req, "text")
    print(post, metadata, config, files, media_type)


def make_handler(req, operators):
    if req.path is "/index/text/":
        return handle_text(operators)
    elif req.path is "/index/image/":
        return handle_image(operators)
    elif req.path is "/index/video":
        return handle_video(operators)
    else:
        raise "Unsupported endpoint."
