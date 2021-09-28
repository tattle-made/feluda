default_config = {"supported_media": ["text", "image", "video"]}


class Search:
    def __init__(self, param, store, operators):
        for operator in param["parameters"]["operators"]:
            self.operators[operator["media_type"]] = operators[operator["type"]]
        self.store = store

    def search(self, post, store):
        if post.type in self.operators.supported_media:
            representation = self.operators[post.type].get_representation(post)
            # get store
            # get the right function make_for_* for that post.
            # save
            doc = {}  # todo how to format the representation?

            res = store(doc)
            return res
        else:
            return "Invalid Post Type"

    def get_routes(self):
        return {
            "search": {"endpoint": "/search", "type": "POST", "handler": self.search}
        }
