import logging

from feluda import config

log = logging.getLogger(__name__)


class Feluda:
    """Main class for Feluda."""

    def __init__(self, config_path: str) -> None:
        """Initialize the Feluda framework with a configuration file.

        Args:
            config_path (str): Path to the configuration file.
        """
        self.config = config.load(config_path)
        self.store = None
        self.operators = None
