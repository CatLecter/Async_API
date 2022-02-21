import pickle
from datetime import timedelta
from typing import Any
import aioredis
from tests.functional.settings import config


class RedisHelper:
    def __init__(self):
        self.redis = await aioredis.create_redis_pool(
            (config.REDIS_HOST, config.REDIS_PORT),
            minsize=10,
            maxsize=20,
        )
        self.ttl = timedelta(60)
        self.expire = int(self.ttl.total_seconds())

    async def set(self, key: str, data: Any) -> None:
        await self.redis.set(key=key, value=pickle.dumps(data), expire=self.expire)

    async def get(self, key: str) -> Any:
        data = await self.redis.get(key=key)
        if not data:
            return None
        data = pickle.loads(data)
        return data
