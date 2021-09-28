from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class PostData:
    post_id: str
    source_id: str
    client_id: str
    media_type: str


@dataclass
class TextPostData(PostData):
    text: str
    media_type: str = "text"


@dataclass
class ImagePostData(PostData):
    media_url: str
    media_type: str = "image"


@dataclass
class VideoPostData(PostData):
    media_url: str
    media_type: str = "video"


@dataclass
class IndexRequestConfig:
    persist: bool = True


@dataclass
class Post:
    type: str
    post_data: PostData
    config: IndexRequestConfig
    metadata: object


@dataclass
class IndexRequestModel:
    post_id: str
    source_id: str
    client_id: str
    media_type: str
    metadata: object = {}
    file_url: str = None
    text_data: str = None
    date_added: datetime = datetime.utcnow()

    @staticmethod
    def FromRequestData(req_data):
        return IndexRequestModel(
            post_id=req_data["post_id"],
            source_id=req_data["source_id"],
            client_id=req_data["client_id"],
            media_type=req_data["media_type"],
            metadata=req_data["metadata"],
            file_url=req_data["media_url"],
            text_data=req_data["text"],
        )

    def get_post_data(self):
        post = {
            "post_id": self.post_id,
            "source_id": self.source_id,
            "client_id": self.client_id,
        }
        if self.file_url is not None:
            post["media_url"] = self.file_url
        if self.text_data is not None:
            post["text_data"] = self.text_data

        return post


def format_req(self, req, media_type):
    if media_type is "text":
        post = TextPostData(**req.form.get("post_data"))
    elif media_type is "image":
        post = ImagePostData(**req.form.get("post_data"))
    elif media_type is "video":
        post = VideoPostData(**req.form.get("post_data"))
    else:
        raise "Unsupported Media Type. Please refer to documentation on : /API/index/#media_type"

    metadata = json.loads(req.form.get("meta_data"))
    config = IndexRequestConfig(**req.form.get("config"))
    files = req.files["media"]

    return (post, metadata, config, files)
