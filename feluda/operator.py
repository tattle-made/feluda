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
            try:
                module_path = f"{operator.type}"
                module = importlib.import_module(module_path)
                module.initialize(operator.parameters)
                self.active_operators[operator.type] = module
            except ImportError as e:
                log.error(f"Error importing module {operator.type}: {e}")
                raise ImportError(f"Error importing module {operator.type}: {e}")
            except Exception as e:
                log.error(f"Error initializing operator {operator.type}: {e}")
                raise Exception(f"Error initializing operator {operator.type}: {e}")

    def get(self):
        return self.active_operators
