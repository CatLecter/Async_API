import asyncio
from time import sleep

import aioredis

from functional.settings import config


async def wait():
    redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    ping = await redis.ping()
    if b'PONG' == ping:
        return True
    return None


if __name__ == "__main__":
    result = False
    while not result:
        try:
            result = asyncio.run(wait())
        except Exception:
            print('sleep')
            sleep(1)
