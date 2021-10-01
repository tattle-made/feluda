from dataclasses import dataclass
from datetime import datetime
import json
from os import stat
from typing import Optional
from werkzeug.datastructures import FileStorage
import requests
import PIL
from io import BytesIO
import numpy as np


@dataclass
class IndexRequestPostData:
    post_id: str
    source_id: str
    client_id: str


@dataclass
class TextPostData(IndexRequestPostData):
    text: Optional[str] = None
    media_type: str = "text"


@dataclass
class ImagePostData(IndexRequestPostData):
    media_url: Optional[str] = None
    media_type: str = "image"

    @staticmethod
    def make_from_url(image_url):
        resp = requests.get(image_url)
        image_bytes = resp.content
        image = PIL.Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {"image": image, "image_array": image_array, "image_bytes": image_bytes}

    def make_from_file(image_path):
        with open(image_path, mode="rb") as file:
            image_bytes = file.read()
            image = PIL.Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {
                "image": image,
                "image_array": image_array,
                "image_bytes": image_bytes,
            }


@dataclass
class VideoPostData(IndexRequestPostData):
    media_url: Optional[str] = None
    media_type: str = "video"


@dataclass
class Config:
    version: str = "0.1"


@dataclass
class Post:
    type: str
    post_data: IndexRequestPostData
    config: Config
    metadata: object
    file: FileStorage or None

    @staticmethod
    def fromRequestPayload(type, request):
        try:
            data = json.load(request.files["data"])
            file = request.files["media"]
            config = data["config"]
            metadata = data["metadata"]
            post = data["post"]
            return Post(
                type=type,
                post_data=TextPostData(**post)
                if (type == "text")
                else ImagePostData(**post)
                if (type == "image")
                else VideoPostData(**post)
                if (type == "video")
                else IndexRequestPostData(**post),
                config=Config(**config),
                metadata=metadata,
                file=file,
            )
        except Exception as e:
            print(e)
            raise Exception("Unknown Structure of Data")


def make_post_from_request(self, req, media_type):
    if media_type is "text":
        post_data = TextPostData(**req.form.get("post"))
    elif media_type is "image":
        post_data = ImagePostData(**req.form.get("post"))
    elif media_type is "video":
        post_data = VideoPostData(**req.form.get("post"))
    else:
        raise "Unsupported Media Type. Please refer to documentation on : /API/index/#media_type"

    metadata = json.loads(req.form.get("metadata"))
    config = Config(**req.form.get("config"))
    files = req.files["media"]

    post = Post(media_type, post_data, config, metadata, files)

    # return (post, metadata, config, files, media_type)
    return post
