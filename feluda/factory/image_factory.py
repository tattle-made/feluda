import logging
import os
import tempfile
from io import BytesIO

import numpy as np
import requests
import wget
from PIL import Image
from requests.exceptions import ConnectTimeout
from werkzeug.datastructures import FileStorage

log = logging.getLogger(__name__)


class ImageFactory:
    @staticmethod
    def make_from_url(image_url: str) -> dict | None:
        try:
            print("1", image_url)
            resp = requests.get(image_url, timeout=(3.05, 5))
            image_bytes = resp.content
            image = Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {
                "image": image,
                "image_array": image_array,
                "image_bytes": image_bytes,
            }
        except ConnectTimeout:
            print("Request has timed out")

    @staticmethod
    def make_from_url_to_path(image_url: str) -> dict | None:
        temp_dir = tempfile.gettempdir()
        temp_url = image_url.split("?", maxsplit=1)[0]
        file_name = temp_url.split("/")[-1]
        image_path = os.path.join(temp_dir, file_name)
        try:
            print("Downloading image from URL")
            wget.download(image_url, out=image_path)
            print("\nImage downloaded")
        except Exception as e:
            print("Error downloading image:", e)
            raise Exception("Error Downloading Image")
        return {"path": image_path}

    @staticmethod
    def make_from_file_on_disk(image_path: str) -> dict:
        with open(image_path, mode="rb") as file:
            image_bytes = file.read()
            image = Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {
                "image": image,
                "image_array": image_array,
                "image_bytes": image_bytes,
            }

    @staticmethod
    def make_from_file_on_disk_to_path(image_path: str) -> dict:
        return {"path": image_path}

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage) -> dict:
        image_bytes = image_data.read()
        image = Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {
            "image": image,
            "image_array": image_array,
            "image_bytes": image_bytes,
        }
