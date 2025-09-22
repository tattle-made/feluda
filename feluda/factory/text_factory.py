import requests
from requests.exceptions import ConnectTimeout
from werkzeug.datastructures import FileStorage


class TextFactory:
    """Factory class for creating text objects from various sources."""

    @staticmethod
    def make_from_url(text_url: str) -> dict:
        """Create a text object from a URL."""
        try:
            response = requests.get(text_url, timeout=(3.05, 5))
            text = response.text
            return {"text": text}
        except ConnectTimeout:
            print("Request has timed out")
            raise Exception("Request has timed out")

    @staticmethod
    def make_from_file_on_disk(text_path: str) -> None:
        """Create a text object from a file on disk."""
        return {"path": text_path}

    @staticmethod
    def make_from_file_in_memory(text_path: FileStorage) -> None:
        """Create a text object from a file on disk."""
        with open(text_path) as file:
            text = file.read()
            return {
                "text": text,
                "text_bytes": file.read().encode("utf-8"),
            }
