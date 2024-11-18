import logging
from feluda import config
from enum import Enum

log = logging.getLogger(__name__)

class Feluda:
    def __init__(self, configPath):
        self.config = config.load(configPath)
        self.store = None
        if self.config.operators:
            from feluda.operator import Operator
            self.operators = Operator(self.config.operators)

    def setup(self):
        if self.operators:
            self.operators.setup()