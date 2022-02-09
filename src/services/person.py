from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Film, Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        doc = await self.elastic.get(index="persons", id=person_id)
        return Person(**doc["_source"])

    async def search_persons(
        self,
        page_size: int,
        page_number: int,
        query: str,
        sort_field: str,
        filter_field: str,
        filter_value: str,
    ):
        # формируем уникальное значение hash, состоящее из строки параметров запроса
        # и используем его как ключ к запросу list[id] персон
        hash_query = str(
            hash(
                f"{query}{filter_field}{filter_value}{sort_field}{page_size}{page_number}"
            )
        )
        list_persons = []
        list_ids = []
        if _list_ids := await self.redis.get(hash_query):
            list_ids = str(_list_ids)[3:-2].replace('"', "").split(",")
        # получаем от redis.get() class bytes (байтовую строку) и переводим его в list[id]
        if list_ids:
            for person_id in list_ids:
                if person_id:
                    person = await self._person_from_cache(person_id)
                    list_persons.append(person)
        if not list_persons:
            list_persons = await self.search_persons_from_elastic(
                page_size,
                page_number,
                query,
                sort_field,
                filter_field,
                filter_value,
            )
            if not list_persons:
                return None
            for _person in list_persons:
                await self._put_person_to_cache(_person)
                list_ids.append(_person.id)
            await self.redis.set(
                key=hash_query,
                value=orjson.dumps(list_ids),
                expire=PERSON_CACHE_EXPIRE_IN_SECONDS,
            )
        return list_persons

    async def search_persons_from_elastic(
        self,
        page_size: int,
        page_number: int,
        query: str,
        sort_field: str,
        filter_field: str,
        filter_value: str,
    ):
        body = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "query": {
                "bool": {
                    "must": {
                        "simple_query_string": {
                            "query": query,
                            "fields": ["full_name"],
                            "default_operator": "or",
                        }
                    },
                    "filter": {"term": {filter_field: filter_value}},
                },
            },
            "sort": [{sort_field: {"order": "asc"}}],
        }
        doc = await self.elastic.search(
            index="persons",
            body=body,
        )
        persons = [Person(**_["_source"]) for _ in doc["hits"]["hits"]]
        return persons

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(
            person.id, person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
