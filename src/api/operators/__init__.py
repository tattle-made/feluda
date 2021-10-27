import logging

log = logging.getLogger(__name__)
import importlib
from core.config import OperatorConfig

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
