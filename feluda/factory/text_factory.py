import requests
from requests.exceptions import ConnectTimeout
from werkzeug.datastructures import FileStorage


class TextFactory:
    @staticmethod
    def make_from_url(text_url: str) -> dict | None:
        try:
            response = requests.get(text_url, timeout=(3.05, 5))
            text = response.text
            return {"text": text}
        except ConnectTimeout:
            print("Request has timed out")

    @staticmethod
    def make_from_file_on_disk(image_path: str) -> None:
        pass

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage) -> None:
        pass
