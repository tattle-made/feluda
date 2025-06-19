import logging

from feluda import config

log = logging.getLogger(__name__)


class Feluda:
    def __init__(self, config_path: str) -> None:
        self.config = config.load(config_path)
        self.store = None
        self.operators = None
        if self.config.operators:
            from feluda.operator import Operator

            self.operators = Operator(self.config.operators)

    def setup(self) -> None:
        if self.operators:
            self.operators.setup()
