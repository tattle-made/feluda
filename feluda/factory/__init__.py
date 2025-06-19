import logging
import warnings
from enum import Enum

from .text_factory import TextFactory

try:
    from .audio_factory import AudioFactory
except ImportError:
    AudioFactory = None
    warnings.warn(
        "AudioFactory is unavailable because 'feluda[audio]' was not installed.",
        ImportWarning,
        stacklevel=2,
    )

try:
    from .image_factory import ImageFactory
except ImportError:
    ImageFactory = None
    warnings.warn(
        "ImageFactory is unavailable because 'feluda[image]' was not installed.",
        ImportWarning,
        stacklevel=2,
    )


try:
    from .video_factory import VideoFactory
except ImportError:
    VideoFactory = None
    warnings.warn(
        "VideoFactory is unavailable because 'feluda[video]' was not installed.",
        ImportWarning,
        stacklevel=2,
    )


log = logging.getLogger(__name__)


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
    def make(cls, media_type: str) -> "MediaType":
        if media_type == "text":
            return cls.TEXT
        if media_type == "image":
            return cls.IMAGE
        if media_type == "video":
            return cls.VIDEO
        if media_type == "audio":
            return cls.AUDIO
        return cls.UNSUPPORTED


media_factory = {
    MediaType.TEXT: TextFactory,
    MediaType.IMAGE: ImageFactory,
    MediaType.VIDEO: VideoFactory,
    MediaType.AUDIO: AudioFactory,
}
