from dataclasses import dataclass

import aiohttp
import pytest
from tests.functional.utils.es_helper import ESHelper
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def create_index():
    """Создаёт индексы перед сессией тестов и
    удаляет их после окончания тестов.
    """

    es_helper = ESHelper()
    await es_helper.create_index()
    yield
    await es_helper.delete_index()
    await es_helper.client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
