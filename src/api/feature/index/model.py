from dataclasses import dataclass
from datetime import datetime
import json
from werkzeug.datastructures import MultiDict, FileStorage


@dataclass
class IndexRequestPostData:
    post_id: str
    source_id: str
    client_id: str
    media_type: str


@dataclass
class TextPostData(IndexRequestPostData):
    text: str
    media_type: str = "text"


@dataclass
class ImagePostData(IndexRequestPostData):
    media_url: str
    media_type: str = "image"


@dataclass
class VideoPostData(IndexRequestPostData):
    media_url: str
    media_type: str = "video"


@dataclass
class IndexRequestConfig:
    persist: bool = True


@dataclass
class Post:
    type: str
    post_data: IndexRequestPostData
    config: IndexRequestConfig
    metadata: object
    files: MultiDict(str, FileStorage)


# @dataclass
# class IndexRequestModel:
#     post_id: str
#     source_id: str
#     client_id: str
#     media_type: str
#     metadata: object = {}
#     file_url: str = None
#     text_data: str = None
#     date_added: datetime = datetime.utcnow()

#     post: PostData = None

#     @staticmethod
#     def FromRequestData(req_data):
#         return IndexRequestModel(
#             post_id=req_data["post_id"],
#             source_id=req_data["source_id"],
#             client_id=req_data["client_id"],
#             media_type=req_data["media_type"],
#             metadata=req_data["metadata"],
#             file_url=req_data["media_url"],
#             text_data=req_data["text"],
#         )

#     def get_post_data(self):
#         post = {
#             "post_id": self.post_id,
#             "source_id": self.source_id,
#             "client_id": self.client_id,
#         }
#         if self.file_url is not None:
#             post["media_url"] = self.file_url
#         if self.text_data is not None:
#             post["text_data"] = self.text_data

#         return post


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
    config = IndexRequestConfig(**req.form.get("config"))
    files = req.files["media"]

    post = Post(media_type, post_data, config, metadata, files)

    # return (post, metadata, config, files, media_type)
    return post
