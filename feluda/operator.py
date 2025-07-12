from abc import ABC, abstractmethod


class Operator(ABC):
    """Base class for all operators in the Feluda framework."""

    def __init__(self) -> None:
        """Initialize the operator."""
        super().__init__()

    @abstractmethod
    def run(self, file_path: str, *args, **kwargs):
        """Execute main logic."""

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources or memory."""

    @abstractmethod
    def state(self) -> dict:
        """Return internal state."""
