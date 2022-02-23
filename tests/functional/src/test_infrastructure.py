import pytest


@pytest.mark.asyncio
async def test_ping_es(create_index):
    es_ping = await create_index.ping()
    assert es_ping is True


# todo: тест по проверке того что индексы создались
# http://127.0.0.1:9200/_aliases ->
# {"persons":{"aliases":{}},"movies":{"aliases":{}},"genres":{"aliases":{}}}


@pytest.mark.asyncio
async def test_ping_redis(create_cache):
    redis_ping = await create_cache.ping()
    assert redis_ping == b"PONG"
