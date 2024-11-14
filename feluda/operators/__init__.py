import logging
import importlib
from feluda.config import OperatorConfig

log = logging.getLogger(__name__)

PACKAGE = "operators"


class Operator:
    def __init__(self, config: OperatorConfig):
        self.active_operators = {}
        self.operators = config.parameters

    def setup(self):
        for operator in self.operators:
            log.info(operator.type)
            # module_path = f"{PACKAGE}.{operator.type}.{operator.type}"
            module_path = f"{operator.type}.{operator.type}"
            print("before import")
            print(module_path)
            module = importlib.import_module(module_path)
            print("after import")
            print(module)
            module.initialize(operator.parameters)
            self.active_operators[operator.type] = module

    def get(self):
        return self.active_operators
