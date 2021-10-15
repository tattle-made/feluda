from .handler import IndexHandler

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

    def __init__(self, store, operators):
        self.operators = operators
        return
        # for operator in param["parameters"]["operators"]:
        #     self.operators[operator["media_type"]] = operators[operator["type"]]
        # self.store = store

    def get_handler(self):
        handler = IndexHandler()
        return handler.make_handler(self.operators)
        # return handler.make_handler(req, self.operators)

    def get_routes(self):
        """
        tuple syntax : (endpoint, method type, handler function)
        """
        return [
            ("/index/text", "index_text", ["POST"]),
            ("/index/image", "index_image", ["POST"]),
            ("/index/video", "index_video", ["POST"]),
            ("/enqueue/text", "enqueue_text", ["POST"]),
            ("/enqueue/image", "enqueue_image", ["POST"]),
            ("/enqueue/video", "enqueue_video", ["POST"]),
            ("/represent/text", "represent_text", ["POST"]),
            ("/represent/image", "represent_image", ["POST"]),
            ("/represent/video", "represent_video", ["POST"]),
        ]
