import json
from dataclasses import dataclass
import os
from pathlib import Path

import aiohttp
import pytest
from tests.functional.settings import config
from utils.es_helper import ESHelper
from elasticsearch import AsyncElasticsearch, ElasticsearchException
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}")
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = config.SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(), headers=response.headers, status=response.status
            )
    return inner


@pytest.fixture(scope="session")
async def create_index(name_index: str, file_index: str):
    """Создаёт индекс для тестов и удаляет его после окончания теста."""

    es_helper = ESHelper()
    await es_helper.create_index(name_index, file_index)
    yield
    await es_helper.delete_index(name_index)
