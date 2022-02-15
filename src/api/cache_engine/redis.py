import pickle
from datetime import timedelta
from typing import Any

from aioredis import Redis

from cache_engine.general import AbstractCache
from core.config import CACHE_TTL


class RedisCache(AbstractCache):
    def __init__(self, redis: Redis, ttl: timedelta = CACHE_TTL):
        self.redis = redis
        self.expire = ttl.total_seconds()

    async def save_to_cache(self, cache_key, data) -> None:
        await self.redis.set(
            cache_key,
            pickle.dumps(data),
            expire=self.expire,
        )

    async def load_from_cache(self, cache_key) -> Any:
        data = await self.redis.get(cache_key)
        if not data:
            return None
        data = pickle.loads(data)
        return data
