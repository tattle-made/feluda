import requests
from requests.exceptions import ConnectTimeout
import PIL
from io import BytesIO
import numpy as np
from werkzeug.datastructures import FileStorage
import wget
from core.models.media import MediaType
import logging
import os

log = logging.getLogger(__name__)


class ImageFactory:
    @staticmethod
    def make_from_url(image_url):
        try:
            print("1", image_url)
            resp = requests.get(image_url, timeout=(3.05, 5))
            image_bytes = resp.content
            image = PIL.Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {"image": image, "image_array": image_array, "image_bytes": image_bytes}
        except ConnectTimeout:
            print('Request has timed out')

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
        try:
            response = requests.get(text_url, timeout=(3.05, 5))
            text = response.text
            return {"text": text}
        except ConnectTimeout:
            print('Request has timed out')

    @staticmethod
    def make_from_file_on_disk(image_path):
        pass

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage):
        pass


class VideoFactory:
    @staticmethod
    def make_from_url(video_url):
        try:
            print("Downloading video from url")
            dl_file = wget.download(video_url)
            print("video downloaded")
        except Exception as e:
            log.exception("Error downloading video:", e)
            raise Exception("Error Downloading Video")
        return {"path": os.path.realpath(dl_file)}

    @staticmethod
    def make_from_file_on_disk(video_path):
        return {"path": video_path}

    @staticmethod
    def make_from_file_in_memory(file_data: FileStorage):
        # save on disk
        fname = file_data.filename
        # TODO: test use tmp folder with path if required
        # fname = "/tmp/" + file_data.filename
        file_data.save(fname)
        return {"path": fname}


class AudioFactory:
    @staticmethod
    def make_from_url(audio_url):
        try:
            print("Downloading audio from url")
            audio_file = wget.download(audio_url)
            print("audio downloaded")
        except Exception as e:
            log.exception("Error downloading audio:", e)
            raise Exception("Error Downloading audio")
        return {"path": os.path.realpath(audio_file)}

    @staticmethod
    def make_from_file_on_disk(audio_path):
        return {"path": audio_path}


media_factory = {
    MediaType.TEXT: TextFactory,
    MediaType.IMAGE: ImageFactory,
    MediaType.VIDEO: VideoFactory,
    MediaType.AUDIO: AudioFactory,
}
