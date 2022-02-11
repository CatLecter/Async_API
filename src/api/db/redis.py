import asyncio
import functools
import logging
import pickle
from datetime import timedelta
from typing import Callable, Optional

import aioredis.errors
from aioredis import Redis

from core.config import CACHE_TTL

logger = logging.getLogger(__name__)
redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


def redis_cache_me(key_function: Callable, ttl: timedelta = CACHE_TTL):
    """Декоратор для кэширования возвращаемого функцией значения в редис."""

    def _decorator(func):
        @functools.wraps(func)
        async def _wrapper(*args, **kwargs):
            cache_key = f'{func.__module__}:{func.__name__}:{key_function(*args, **kwargs)}'

            try:
                pickled_data = await redis.get(cache_key)
                if pickled_data is not None:
                    data = pickle.loads(pickled_data)
                    logger.info(f'Get data from Redis by key "{cache_key}".')
                    return data
            except aioredis.errors.RedisError as e:
                logger.error(e)

            data = await func(*args, **kwargs)
            logger.info(f'Put data to Redis by key "{cache_key}".')
            pickled_data = pickle.dumps(data)
            asyncio.create_task(
                redis.set(cache_key, pickled_data, expire=int(ttl.total_seconds()))
            )
            return data

        return _wrapper

    return _decorator
