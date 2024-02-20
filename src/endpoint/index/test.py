from .model import Post
from enum import Enum


class MediaMode(Enum):
    FILE = 1
    URL = 2
    LOCAL_FILE_PATH = 3


class MediaType(Enum):
    TEXT = 1
    IMAGE = 2
    VIDEO = 3


class IndexResult(Enum):
    SUCCESS = 1
    FAILURE = 2


payload = {"post": {}, "metadata": {}, "config": {}}
post = Post.fromRequestPayload(payload["post"]["media_type"], payload)

# mode can be 'file' or 'url'
index_handler = IndexHandler.make(media_type=post.type, mode=MediaMode.URL)
result = index_handler(post)
add_to_report_queue(result)


class IndexHandler:
    @staticmethod
    def make(media_type: MediaType, mode: MediaMode):
        if media_type is MediaType.TEXT:
            return IndexTextHandler.make(mode)
        elif media_type is MediaType.TEXT:
            return IndexTextHandler.make(mode)
        elif media_type is MediaType.TEXT:
            return IndexTextHandler.make(mode)
        else:
            return AttributeError
