import logging

log = logging.getLogger(__name__)
import importlib
from core.config import OperatorConfig

PACKAGE = "core.operators"


class Operator:
    def __init__(self, config: OperatorConfig):
        self.active_operators = {}
        operators = config.parameters
        for operator in operators:
            # print(operator["type"], ":", operator["parameters"])
            log.info(operator.type)
            self.active_operators[operator.type] = importlib.import_module(
                "." + operator.type, package=PACKAGE
            )
            self.active_operators[operator.type].initialize(operator.parameters)

    def get(self):
        return self.active_operators
