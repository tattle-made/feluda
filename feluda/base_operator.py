from abc import ABC, abstractmethod


class BaseOperator(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run(self, file_path: str, *args, **kwargs):
        """Main execution logic."""

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources or memory."""

    @abstractmethod
    def state(self) -> dict:
        """Return internal state (e.g., is model loaded)."""
