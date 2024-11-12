from enum import Enum


class MediaMode(Enum):
    UNSUPPORTED = "unsupported"
    FILE = "file"
    URL = "url"
    LOCAL_FILE_PATH = "local_file_path"


class MediaType(Enum):
    UNSUPPORTED = "unsupported"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

    @classmethod
    def make(media_type):
        if media_type == "text":
            return MediaType.TEXT
        elif media_type == "image":
            return MediaType.IMAGE
        elif media_type == "video":
            return MediaType.VIDEO
        elif media_type == "audio":
            return MediaType.AUDIO
        else:
            return MediaType.UNSUPPORTED
