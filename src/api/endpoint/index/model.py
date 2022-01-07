from dataclasses import dataclass
from enum import Enum
import json
from typing import Optional
import typing
from core.models.media import MediaMode, MediaType
from werkzeug.datastructures import FileStorage
import logging
from core.models.media_factory import media_factory

log = logging.getLogger(__name__)


@dataclass
class IndexRequestPostData:
    id: str
    datasource_id: Optional[str]
    client_id: Optional[str]


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


@dataclass
class Post:
    type: MediaType
    mode: MediaMode
    post_data: IndexRequestPostData
    config: Config
    metadata: object
    file: FileStorage or None

    @staticmethod
    def OldfromRequestPayload(request):
        try:
            data = json.load(request.files["data"])
            file = request.files.get("media", None)
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
            print("---->", e)
            log.exception("Unknown Structure of Data")
            raise Exception("Unknown Structure of Data")

    @staticmethod
    def fromRequestPayload(data, file=None):
        try:
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
            print("---->", e)
            log.exception("Unknown Structure of Data")
            raise Exception("Unknown Structure of Data")

    @staticmethod
    def fromRequestPayloadJSON(data, file=None):
        try:
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
            print("---->", e)
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
