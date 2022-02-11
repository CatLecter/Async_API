from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MatchAll
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis, redis_cache_me
from models.genre import Genre, GenreBrief


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @redis_cache_me(key_function=lambda self, genre_uuid: f'genre_uuid:{genre_uuid}')
    async def get_by_uuid(self, genre_uuid: str) -> Optional[Genre]:
        """Возвращает жанр по UUID."""
        try:
            doc = await self.elastic.get(index='genres', id=genre_uuid)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    @redis_cache_me(key_function=lambda self: 'genre_list')
    async def genre_list(self) -> List[GenreBrief]:
        """Возвращает список жанров."""
        genres = await self._get_genre_list_from_elastic()
        return genres

    async def _get_genre_list_from_elastic(self) -> List[GenreBrief]:
        search = Search(using=self.elastic)
        search = search.query(MatchAll())
        body = search.to_dict()
        docs = await self.elastic.search(index='genres', body=body, size=500)
        result = [GenreBrief(**doc['_source']) for doc in docs['hits']['hits']]
        result.sort(key=lambda genre: genre.name)
        return result


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
