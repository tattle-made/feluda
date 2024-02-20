import logging
import pprint
import os

logging.basicConfig(level="INFO")
pp = pprint.PrettyPrinter(indent=2)


class Logger:
    def __init__(self, moduleName):
        self.environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
        self.log = logging.getLogger(moduleName)

    def info(self, msg):
        self.log.info(msg)

    def debug(self, msg):
        if self.environment == "DEVELOPMENT":
            self.log.debug(msg)

    def exception(self, msg):
        self.log.exception(msg)

    def prettyprint(self, msg):
        pp.pprint(msg)
