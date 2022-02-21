from tests.functional.utils.es_helper import ESHelper
from tests.functional.utils.redis_helper import RedisHelper


async def test_ping_es():
    es_helper = ESHelper()
    es_ping = await es_helper.client.ping()
    assert es_ping is True


async def test_ping_redis():
    redis_helper = RedisHelper()
    redis_ping = await redis_helper.redis.ping()
    assert redis_ping is True
