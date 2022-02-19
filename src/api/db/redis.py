import logging
from typing import Optional

import aioredis.errors
from aioredis import Redis

from core import config

logger = logging.getLogger(__name__)
redis: Optional[Redis] = None


async def get_redis() -> Redis:
    """Возвращает объект для асинхронного общения с сервисами Redis.
    Функция понадобится при внедрении зависимостей."""
    return redis


async def redis_connect():
    """Устанавливает подключение к сервису Redis."""
    global redis
    redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    logger.info('Successfully connected to redis server.')
