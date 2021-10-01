import importlib

PACKAGE = "operators"


def intialize(config):
    active_operators = {}
    operators = config["parameters"]["operators"]
    for operator in operators:
        print(operator["type"], ":", operator["parameters"])
        active_operators[operator["type"]] = importlib.import_module(
            "." + operator["type"], package=PACKAGE
        )
        active_operators[operator["type"]].initialize(operator["parameters"])
    return active_operators


# def run(operator, post):
#     return operator.run(post)


# operators = {
#     "default": default,
#     "text_fulltext_rep": default,
#     "vid_vec_rep_resnet": default,
#     "composite_image_text_indexer": composite_image_text_indexer,
# }
