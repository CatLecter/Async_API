import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from multidict import CIMultiDictProxy

from tests.functional.settings import config
from tests.functional.utils.es_helper import ESHelper
from tests.functional.utils.redis_helper import RedisHelper


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    print("123")
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def create_index():
    """Создаёт индексы перед сессией тестов и
    удаляет их после окончания тестов.
    """

    es_helper = ESHelper()
    await es_helper.create_index()
    await es_helper.load_data()
    yield es_helper.client
    await es_helper.delete_index()
    await es_helper.client.close()


@pytest.fixture(scope="session")
async def create_cache():
    """Создаёт объект кэша."""
    redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT))
    await redis.flushall()
    yield redis
    await redis.flushall()
    redis.close()
    await redis.wait_closed()
