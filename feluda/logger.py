import logging
import os
import pprint

logging.basicConfig(level="INFO")
pp = pprint.PrettyPrinter(indent=2)


class Logger:
    """Logger class to handle logging."""

    def __init__(self, module_name: str) -> None:
        """Initialize the logger with a module name.

        Args:
            module_name (str): Name of the module for logging.
        """
        self.environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
        self.log = logging.getLogger(module_name)

    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an info message."""
        self.log.info(msg, *args, **kwargs)

    def debug(self, msg: str) -> None:
        """Log a debug message if in development environment."""
        if self.environment == "DEVELOPMENT":
            self.log.debug(msg)

    def exception(self, msg: str) -> None:
        """Log an exception message."""
        self.log.exception(msg)

    @staticmethod
    def prettyprint(msg: str) -> None:
        """Pretty-print a message."""
        pp.pprint(msg)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log an error message."""
        self.log.error(self, msg, *args, **kwargs)
