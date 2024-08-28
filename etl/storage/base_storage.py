import abc
from typing import Any, Dict


class BaseStorage(abc.ABC):

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Save state to the storage."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Retrieve state from the storage."""

    @abc.abstractmethod
    def get_state(self, key: str) -> Any:
        """Get state from the storage."""
