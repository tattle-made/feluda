import logging

log = logging.getLogger(__name__)
import importlib
from api.core.config import OperatorConfig

PACKAGE = "operators"


def intialize(config: OperatorConfig):
    active_operators = {}
    operators = config.parameters
    for operator in operators:
        # print(operator["type"], ":", operator["parameters"])
        log.info(operator.type)
        active_operators[operator.type] = importlib.import_module(
            "." + operator.type, package=PACKAGE
        )
        active_operators[operator.type].initialize(operator.parameters)
    return active_operators


# def run(operator, post):
#     return operator.run(post)


# operators = {
#     "default": default,
#     "text_fulltext_rep": default,
#     "vid_vec_rep_resnet": default,
#     "composite_image_text_indexer": composite_image_text_indexer,
# }
