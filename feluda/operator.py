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
            # Try to import the operator module with the full path first
            try:
                module_path = f"operators.{operator.type}.{operator.type}"
                module = importlib.import_module(module_path)
            except ImportError:
                # Fall back to direct import if the full path doesn't work
                try:
                    module_path = f"{operator.type}"
                    module = importlib.import_module(module_path)
                except ImportError as e:
                    log.error(f"Failed to import operator module {operator.type}: {e}")
                    raise
            module.initialize(operator.parameters)
            self.active_operators[operator.type] = module

    def get(self):
        return self.active_operators
