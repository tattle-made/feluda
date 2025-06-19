import importlib
import logging

from feluda.config import OperatorConfig

log = logging.getLogger(__name__)


class Operator:
    def __init__(self, config: OperatorConfig) -> None:
        self.active_operators = {}
        self.operators = config.parameters

    def setup(self) -> None:
        for operator in self.operators:
            log.info(operator.type)
            module_path = f"{operator.type}"
            module = importlib.import_module(module_path)
            module.initialize(operator.parameters)
            self.active_operators[operator.type] = module

    def get(self) -> dict:
        return self.active_operators
