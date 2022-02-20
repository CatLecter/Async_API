from dataclasses import dataclass
import os

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

SERVICE_URL = 'http://127.0.0.1:8000'
ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elastic')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
async def es_client():
    host = f"{ELASTIC_HOST}:{ELASTIC_PORT}"
    client = AsyncElasticsearch(hosts=host)
    yield client
    await client.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        url = SERVICE_URL + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


async def create_es_index(es_client, index_body):
    """Создание индекса ElasticSearch."""
    await es_client.indices.create(index=index_name, body=index_body, ignore=400)













#
# @pytest.fixture(scope="session")
# async def redis_client():
#     redis = await aioredis.create_redis_pool(
#         (settings.redis_host, settings.redis_port),
#         minsize=10, maxsize=20
#     )
#     yield redis
#     redis.close()
#
#
# @pytest.fixture()
# async def es_from_snapshot(es_client):
#     """
#     Fill ElasticSearch data from snapshot and cleanup after tests.
#     """
#     snapshots = SnapshotClient(es_client)
#     body = {
#         "type": "fs",
#         "settings": {
#             "location": os.path.join(settings.es_snapshot_loc,
#                                      settings.es_snapshot_repo)
#         }
#     }
#     await snapshots.create_repository(repository=settings.es_snapshot_repo,
#                                       body=body,
#                                       verify=True)
#     await snapshots.restore(repository=settings.es_snapshot_repo,
#                             snapshot="snapshot_1",
#                             wait_for_completion=True)
#
#     yield
#     # Cleanup
#     indices = await es_client.indices.get_alias()
#     for index in indices.keys():
#         await es_client.indices.delete(index=index)
#     await snapshots.delete_repository(repository=settings.es_snapshot_repo)

#
#
#
#
# def read_json_file(file_path):
#     with open(file_path) as json_file:
#         json_data = json.load(json_file)
#     return json_data
#
#

#
#
# async def load_data_in_index(es_client, index_name):
#     data_path = settings.load_data_dir.joinpath(f"{index_name}.json")
#     data = read_json_file(data_path)
#     await async_bulk(es_client, data, index=index_name)
#
#     items = {}
#     start_time = datetime.now()
#
#     while not items.get("count"):
#         items = await es_client.count(index=index_name)
#         seconds = (datetime.now() - start_time).seconds
#
#         if seconds >= settings.load_index_timeout:
#             raise TimeoutError(
#                 f"Time-out for loading data into ES index {index_name}."
#             )
#
#
# async def initialize_es_index(es_client, index_name):
#     await create_index(es_client, index_name)
#     await load_data_in_index(es_client, index_name)
#
#
# @pytest.fixture(scope="session")
# def event_loop():
#     return asyncio.get_event_loop()
#
#
# @pytest.fixture(scope="session")
# async def initialize_environment(es_client, redis_client):
#     for index in settings.es_indexes:
#         await initialize_es_index(es_client, index)
#     yield
#     await redis_client.flushall()
#     for index in settings.es_indexes:
#         await es_client.indices.delete(index=index, ignore=[400, 404])
#
#
# @pytest.fixture(scope="function")
# async def expected_json_response(request):
#     """
#     Loads expected response from json file with same filename as function name
#     """
#     file = settings.expected_response_dir.joinpath(f"{request.node.name}.json")
#     async with aiofiles.open(file) as f:
#         content = await f.read()
#         response = json.loads(content)
#     return response
