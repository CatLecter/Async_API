from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Nested, Term
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis, redis_cache_me
from models.film import Film, FilmBrief, FilmFilterType, FilmSortingType
from models.general import Page


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @redis_cache_me(key_function=lambda self, film_uuid: f'film_uuid:{film_uuid}')
    async def get_by_uuid(self, film_uuid: str) -> Optional[Film]:
        """Возвращает фильм по UUID."""
        try:
            doc = await self.elastic.get(index='movies', id=film_uuid)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def get_search_result_page(
        self, query: str, page: int, size: int
    ) -> Page[FilmBrief]:
        """Ищет фильмы по названию или описанию. Не кеширует результаты, так как вариантов может быть очень много."""
        film_page = await self._get_film_page_from_elastic(query=query, page=page, size=size,)
        return film_page

    @redis_cache_me(
        key_function=lambda self, sort, filter_type, filter_value, page, size: f'sort:{sort.value},filter_type:{filter_type},filter_value:{filter_value},page:{page},size:{size}'
    )
    async def get_sort_filter_page(
        self,
        sort: FilmSortingType,
        filter_type: FilmFilterType,
        filter_value: str,
        page: int,
        size: int,
    ) -> Page[FilmBrief]:
        """Возвращает список фильмов с фильтрацией и сортировкой."""
        film_page = await self._get_film_page_from_elastic(
            sort=sort,
            filter_type=filter_type,
            filter_value=filter_value,
            page=page,
            size=size,
        )
        return film_page

    async def _get_film_page_from_elastic(
        self,
        query: str = None,
        sort: FilmSortingType = None,
        filter_type: FilmFilterType = None,
        filter_value: str = None,
        page: int = None,
        size: int = None,
    ) -> Page[FilmBrief]:
        try:
            search = Search(using=self.elastic)
            if query:
                search = search.query(
                    MultiMatch(
                        query=query,
                        fields=['title^3', 'description'],
                        operator='and',
                        fuzziness='AUTO',
                    )
                )
            if sort:
                search = search.sort(sort.value)
            if filter_type:
                if filter_type == FilmFilterType.genre:
                    search = search.query(
                        Nested(path='genres', query=Term(genres__uuid=filter_value))
                    )
                elif filter_type == FilmFilterType.person:
                    search = search.query(
                        Nested(path='directors', query=Term(directors__uuid=filter_value))
                        | Nested(path='writers', query=Term(writers__uuid=filter_value))
                        | Nested(path='actors', query=Term(actors__uuid=filter_value))
                    )
                elif filter_type == FilmFilterType.director:
                    search = search.query(
                        Nested(path='directors', query=Term(directors__uuid=filter_value))
                    )
                elif filter_type == FilmFilterType.writer:
                    search = search.query(
                        Nested(path='writers', query=Term(writers__uuid=filter_value))
                    )
                elif filter_type == FilmFilterType.actor:
                    search = search.query(
                        Nested(path='actors', query=Term(actors__uuid=filter_value))
                    )
            start = (page - 1) * size
            end = start + size
            search = search[start:end]
            body = search.to_dict()
            docs = await self.elastic.search(index='movies', body=body)
        except NotFoundError:
            return Page()

        film_page = Page(
            items=[FilmBrief(**doc['_source']) for doc in docs['hits']['hits']],
            total=docs['hits']['total']['value'],
            page=page,
            size=size,
        )

        return film_page


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
