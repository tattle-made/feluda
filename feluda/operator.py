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
            #imports the operator module with the full path first
            try:
                module_path = f"{operator.type}"
                module = importlib.import_module(module_path)
                module.initialize(operator.parameters)
                self.active_operators[operator.type] = module
                log.info(f"Successfully imported {operator.type} directly")
            except (ImportError, ModuleNotFoundError):
                # Fallback to the old path structure if direct import fails
                try:
                    module_path = f"operators.{operator.type}.{operator.type}"
                    module = importlib.import_module(module_path)
                    module.initialize(operator.parameters)
                    self.active_operators[operator.type] = module
                    log.info(f"Successfully imported {operator.type} from operators package")
                except (ImportError, ModuleNotFoundError):
                    #Trying the original path as last resort
                    module_path = f"operators.{operator.type}"
                    module = importlib.import_module(module_path)
                    module.initialize(operator.parameters)
                    self.active_operators[operator.type] = module
                    log.info(f"Successfully imported {operator.type} from operators package")

    def get(self):
        return self.active_operators
