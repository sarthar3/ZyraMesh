from typing import Optional, Any
from app.core.config import settings
from app.core.logging import logger

class MockRedisClient:
    """In-memory key-value cache fallback when real Redis is unavailable"""
    def __init__(self):
        self._store = {}

    def get(self, key: str) -> Optional[str]:
        return self._store.get(key)

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self._store[key] = str(value)
        return True

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def ping(self) -> bool:
        return True


class RedisManager:
    def __init__(self):
        self._client = None
        self._is_mock = True

    def init_redis(self):
        if settings.REDIS_URL:
            try:
                import redis
                client = redis.from_url(settings.REDIS_URL, socket_timeout=2.0)
                client.ping()
                self._client = client
                self._is_mock = False
                logger.info("Connected to Redis server successfully.")
                return
            except Exception as e:
                logger.warning(f"Could not connect to Redis server ({e}). Falling back to MockRedisClient.")

        self._client = MockRedisClient()
        self._is_mock = True

    def get_client(self):
        if self._client is None:
            self.init_redis()
        return self._client

    def check_connection(self) -> dict:
        client = self.get_client()
        try:
            client.ping()
            return {
                "status": "healthy",
                "mode": "mock_in_memory" if self._is_mock else "redis_server"
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

redis_manager = RedisManager()
