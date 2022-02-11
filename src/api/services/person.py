from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis, redis_cache_me
from models.general import Page
from models.person import Person, PersonBrief


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @redis_cache_me(key_function=lambda self, person_uuid: f'person_uuid:{person_uuid}')
    async def get_by_uuid(self, person_uuid: str) -> Optional[Person]:
        """Возвращает персону по UUID."""
        try:
            doc = await self.elastic.get(index='persons', id=person_uuid)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def get_search_result_page(
        self, query: str, page: int, size: int
    ) -> Page[PersonBrief]:
        """Ищет персон по имени. Не кеширует результаты, так как вариантов может быть очень много."""
        person_page = await self._get_person_page_from_elastic(
            query=query, page=page, size=size,
        )
        return person_page

    async def _get_person_page_from_elastic(
        self, query: str = None, page: int = None, size: int = None,
    ) -> Page[PersonBrief]:
        try:
            search = Search(using=self.elastic)
            if query:
                search = search.query(
                    Match(full_name={'query': query, 'fuzziness': 'AUTO', 'operator': 'and'})
                )
            start = (page - 1) * size
            end = start + size
            search = search[start:end]
            body = search.to_dict()
            docs = await self.elastic.search(index='persons', body=body)
        except NotFoundError:
            return Page()

        person_page = Page(
            items=[PersonBrief(**doc['_source']) for doc in docs['hits']['hits']],
            total=docs['hits']['total']['value'],
            page=page,
            size=size,
        )

        return person_page


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
