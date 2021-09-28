 from api import operators
from .handlers import make_handler

default_config = {"supported_media": ["text", "image", "video"]}


class IndexController:
    """
    features :
        index post
            post_data : text or image or video
            config : persist : true or false
            metadata : object
            via file or media_url or plain text

        // API
        support File with JSON
        support JSON
    """
    def __init__(self, param, store, operators):
        for operator in param["parameters"]["operators"]:
            self.operators[operator["media_type"]] = operators[operator["type"]]
        self.store = store

    def get_handler(self, req):
        return make_handler(req, self.operators)
        

    def get_routes(self):
        """
        tuple syntax : (endpoint, method type, handler function)
        """
        return [
            ("/index/text/", "POST"),
            ("/index/image/", "POST"),
            ("/index/video", "POST"),
        ]
