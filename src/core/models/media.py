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
        if media_type is "text":
            return MediaType.TEXT
        elif media_type is "image":
            return MediaType.IMAGE
        elif media_type is "video":
            return MediaType.VIDEO
        elif media_type is "audio":
            return MediaType.AUDIO
        else:
            return MediaType.UNSUPPORTED
