from typing import Any

from storage.base_storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        data = self.storage.get_state(key)
        return data if data else None
