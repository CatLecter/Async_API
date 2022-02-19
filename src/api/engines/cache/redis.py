import pickle
from datetime import timedelta
from typing import Any

from aioredis import Redis

from engines.cache.general import AbstractCache


class RedisCache(AbstractCache):
    """
    Реализация кеширования на основе сервиса Redis.
    """

    def __init__(self, redis: Redis, ttl: timedelta = 60):
        self.redis = redis
        self.expire = ttl.total_seconds()

    async def save_to_cache(self, cache_key: str, data: Any) -> None:
        """Сохраняет данные в кэш."""
        await self.redis.set(
            key=cache_key, value=pickle.dumps(data), expire=self.expire,
        )

    async def load_from_cache(self, cache_key: str) -> Any:
        """Загружает данные из кэша."""
        data = await self.redis.get(key=cache_key)
        if not data:
            return None
        data = pickle.loads(data)
        return data
