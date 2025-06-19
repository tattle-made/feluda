import logging
import os
import pprint

logging.basicConfig(level="INFO")
pp = pprint.PrettyPrinter(indent=2)


class Logger:
    def __init__(self, module_name: str) -> None:
        self.environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
        self.log = logging.getLogger(module_name)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.log.info(msg, *args, **kwargs)

    def debug(self, msg: str) -> None:
        if self.environment == "DEVELOPMENT":
            self.log.debug(msg)

    def exception(self, msg: str) -> None:
        self.log.exception(msg)

    @staticmethod
    def prettyprint(msg: str) -> None:
        pp.pprint(msg)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.log.error(self, msg, *args, **kwargs)
