import importlib
import logging

from feluda.config import OperatorConfig

log = logging.getLogger(__name__)


class Operator:
    def __init__(self, config: OperatorConfig):
        self.active_operators = {}
        self.operators = config.parameters

    def setup(self):
        for operator in self.operators:
            log.info(operator.type)
            module_path = f"{operator.type}"
            module = importlib.import_module(module_path)
            module.initialize(operator.parameters)
            self.active_operators[operator.type] = module

    def get(self):
        return self.active_operators
