import logging
import os
import pprint

logging.basicConfig(level="INFO")
pp = pprint.PrettyPrinter(indent=2)


class Logger:
    def __init__(self, moduleName):
        self.environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
        self.log = logging.getLogger(moduleName)

    def info(self, msg, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def debug(self, msg):
        if self.environment == "DEVELOPMENT":
            self.log.debug(msg)

    def exception(self, msg):
        self.log.exception(msg)

    def prettyprint(self, msg):
        pp.pprint(msg)

    def error(self, msg, *args, **kwargs):
        self.log.error(self, msg, *args, **kwargs)
