from core.feluda import Feluda
from .handler import IndexHandler

default_config = {"supported_media": ["text", "image", "video"]}


class IndexEndpoint:
    def __init__(self, feluda: Feluda):
        self.feluda = feluda

    def get_handler(self):
        handler = IndexHandler(self.feluda)
        return handler.make_handler()

    def get_routes(self):
        """
        tuple syntax : (endpoint, method type, handler function)
        """
        return [
            ("/index", "index", ["POST"]),
        ]
