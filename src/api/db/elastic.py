import logging
from typing import Optional

import backoff
from elasticsearch import AsyncElasticsearch

from core import config
from core.utils import backoff_hdlr

logger = logging.getLogger(__name__)
es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    """Возвращает объект для асинхронного общения с сервисами ElasticSearch.
    Функция понадобится при внедрении зависимостей."""
    return es


@backoff.on_exception(backoff.expo, ConnectionError, on_backoff=backoff_hdlr)
async def elastic_connect():
    """Устанавливает подключение к сервису ElasticSearch."""
    global es
    es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    result = await es.ping()
    if not result:
        raise ConnectionError('The ElasticSearch server is not responding.')
    logger.info('Successfully connected to elasticsearch server.')


async def elastic_disconnect():
    """Закрывает подключение к сервису ElasticSearch."""
    global es
    await es.close()
    logger.info('Successfully disconnected from elasticsearch server.')
