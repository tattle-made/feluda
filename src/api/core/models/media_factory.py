import requests
import PIL
from io import BytesIO
import numpy as np
from werkzeug.datastructures import FileStorage
import wget
from core.models.media import MediaType
import logging

log = logging.getLogger(__name__)


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

    @staticmethod
    def make_from_file_in_memory(file_data: FileStorage):
        # save on disk
        return {"path": "file_path_on_disk"}


media_factory = {
    MediaType.TEXT: TextFactory,
    MediaType.IMAGE: ImageFactory,
    MediaType.VIDEO: VideoFactory,
}
