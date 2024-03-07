import logging
import importlib
from core.config import OperatorConfig

log = logging.getLogger(__name__)

PACKAGE = "core.operators"


class Operator:
    def __init__(self, config: OperatorConfig):
        self.active_operators = {}
        self.operators = config.parameters

    def setup(self):
        for operator in self.operators:
            # print(operator["type"], ":", operator["parameters"])
            log.info(operator.type)
            self.active_operators[operator.type] = importlib.import_module(
                "." + operator.type, package=PACKAGE
            )
            self.active_operators[operator.type].initialize(operator.parameters)

    def get(self):
        return self.active_operators
