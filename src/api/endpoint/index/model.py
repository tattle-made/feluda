from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
from os import stat, path
from typing import Optional
import typing
from core.models.media import MediaMode, MediaType
from werkzeug.datastructures import FileStorage
import requests
import PIL
from io import BytesIO
import numpy as np
import logging
import wget

log = logging.getLogger(__name__)


@dataclass
class IndexRequestPostData:
    id: str
    datasource_id: str
    client_id: str


@dataclass
class TextPostData(IndexRequestPostData):
    text: Optional[str] = None
    media_url: Optional[str] = None
    media_type: str = "text"


@dataclass
class ImagePostData(IndexRequestPostData):
    media_url: Optional[str] = None
    media_type: str = "image"


@dataclass
class VideoPostData(IndexRequestPostData):
    media_url: Optional[str] = None
    media_type: str = "video"


class ConfigMode(Enum):
    STORE = "store"
    ENQUEUE = "enqueue"
    REFLECT = "reflect"


@dataclass
class Config:
    version: str = "0.1"
    mode: ConfigMode = ConfigMode.ENQUEUE


post_factory = {
    "text": TextPostData,
    "image": ImagePostData,
    "video": VideoPostData,
}


class ImageFactory:
    @staticmethod
    def make_from_url(image_url):
        print("1", image_url)
        resp = requests.get(image_url)
        image_bytes = resp.content
        image = PIL.Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {"image": image, "image_array": image_array, "image_bytes": image_bytes}

    @staticmethod
    def make_from_file_on_disk(image_path):
        with open(image_path, mode="rb") as file:
            image_bytes = file.read()
            image = PIL.Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {
                "image": image,
                "image_array": image_array,
                "image_bytes": image_bytes,
            }

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage):
        image_bytes = image_data.read()
        image = PIL.Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {
            "image": image,
            "image_array": image_array,
            "image_bytes": image_bytes,
        }


class TextFactory:
    @staticmethod
    def make_from_url(text_url):
        response = requests.get(text_url)
        text = response.text
        return {"text": text}

    @staticmethod
    def make_from_file_on_disk(image_path):
        pass

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage):
        pass


class VideoFactory:
    @staticmethod
    def make_from_url(video_url):
        fname = "/tmp/vid.mp4"
        try:
            print("Downloading video from url")
            wget.download(video_url, out=fname)
            print("video downloaded")
        except Exception as e:
            log.exception("Error downloading video")
            raise Exception("Error Downloading Video")
        return {"path": fname}

    @staticmethod
    def make_from_file_on_disk(video_path):
        return {"path": video_path}


media_factory = {
    MediaType.TEXT: TextFactory,
    MediaType.IMAGE: ImageFactory,
    MediaType.VIDEO: VideoFactory,
}


@dataclass
class Post:
    type: MediaType
    mode: MediaMode
    post_data: IndexRequestPostData
    config: Config
    metadata: object
    file: FileStorage or None

    @staticmethod
    def fromRequestPayload(request):
        try:
            data = json.load(request.files["data"])
            file = request.files["media"]
            metadata = data["metadata"]
            post = data["post"]
            type = MediaType(post["media_type"])
            return Post(
                type=type,
                mode=MediaMode.URL,
                post_data=post_factory[type.value](**post),
                config=Config(
                    version=data["config"]["version"],
                    mode=ConfigMode(data["config"]["mode"]),
                ),
                metadata=metadata,
                file=file,
            )
        except Exception as e:
            log.exception("Unknown Structure of Data")
            raise Exception("Unknown Structure of Data")

    def getMedia(self) -> typing.IO:
        if self.mode == MediaMode.URL:
            media = media_factory[self.type].make_from_url(self.post_data.media_url)
            return media
        if self.mode == MediaMode.FILE:
            pass
        if self.mode == MediaMode.LOCAL_FILE_PATH:
            pass
        else:
            raise Exception("Unsupported Media Mode")
