import asyncio
from time import sleep
from log_utils import get_logger
import logging

from functional.settings import config

logger = get_logger(__name__)
async def wait():
    pass
    # try:
    #     logger.debug('Подключение к базе данных Elasticsearch...')
    #     conf = {
    #         'host': settings.elastic.host,
    #     }
    #     connection = Elasticsearch([conf])
    #     logger.debug('Успех!')
    #     return connection
    # except Exception as e:
    #     logger.error(e)
    #     raise e


if __name__ == "__main__":
    result = False
    while not result:
        try:
            result = asyncio.run(wait())
        except Exception:
            logger.log(logging.DEBUG, 'sleep')
            sleep(1)
