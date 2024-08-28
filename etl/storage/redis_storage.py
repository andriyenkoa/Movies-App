from dotenv import load_dotenv
import json

import redis
from typing import Any, Dict

from storage.base_storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis_conn: redis.Redis):
        self._redis = redis_conn

    def save_state(self, state: Dict[str, Any]) -> None:
        for key, value in state.items():
            self._redis.set(key, json.dumps(value))

    def retrieve_state(self) -> Dict[str, Any]:
        keys = self._redis.keys()
        data = {}
        for key in keys:
            key_str = key.decode('utf-8')  # Decode key from bytes to string
            value = self._redis.get(key_str)
            if value:
                data[key_str] = json.loads(value.decode('utf-8'))  # Decode value and load from JSON
            else:
                data[key_str] = None
        return data

    def get_state(self, key: str) -> Any:
        value = self._redis.get(key)
        if value:
            return json.loads(value.decode('utf-8'))
        return None
