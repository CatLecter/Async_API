from functools import lru_cache
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        doc = await self.elastic.get(index="genres", id=genre_id)
        return Genre(**doc["_source"])

    async def search_genres(
        self,
        page_size: int,
        page_number: int,
        query: str,
    ):
        # формируем уникальное значение hash, состоящее из строки параметров запроса
        # и используем его как ключ к запросу list[id] жанров
        hash_query = str(hash(f"{query}{page_size}{page_number}"))
        list_genres = []
        list_ids = []
        if _list_ids := await self.redis.get(hash_query):
            list_ids = str(_list_ids)[3:-2].replace('"', "").split(",")
        # получаем от redis.get() class bytes (байтовую строку) и переводим его в list[id]
        if list_ids:
            for genre_id in list_ids:
                if genre_id:
                    genre = await self._genre_from_cache(genre_id)
                    list_genres.append(genre)
        if not list_genres:
            list_genres = await self.search_genres_from_elastic(
                page_size,
                page_number,
                query,
            )
            if not list_genres:
                return None
            for _genre in list_genres:
                await self._put_genre_to_cache(_genre)
                list_ids.append(_genre.id)
            await self.redis.set(
                key=hash_query,
                value=orjson.dumps(list_ids),
                expire=GENRE_CACHE_EXPIRE_IN_SECONDS,
            )
        return list_genres

    async def search_genres_from_elastic(
        self,
        page_size: int,
        page_number: int,
        query: str,
    ):
        body = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "query": {
                "bool": {
                    "must": {
                        "simple_query_string": {
                            "query": query,
                            "fields": ["name"],
                            "default_operator": "or",
                        }
                    },
                },
            },
        }
        doc = await self.elastic.search(
            index="genres",
            body=body,
        )
        genres = [Genre(**_["_source"]) for _ in doc["hits"]["hits"]]
        return genres

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(
            genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
