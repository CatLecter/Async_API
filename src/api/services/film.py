from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmBrief, FilmFilterType, FilmSortingType
from models.general import Page
from search.elastic import ElasticSearchEngine
from search.general import SearchEngine, SearchParams


class FilmService:
    def __init__(self, redis: Redis, search_engine: SearchEngine):
        self.table = 'movies'
        self.redis = redis
        self.search_engine = search_engine

    async def get_by_uuid(self, uuid: str) -> Page[Film]:
        """Возвращает фильм по UUID."""
        result = await self.search_engine.get_by_pk(table=self.table, pk=uuid)

        film_page = Page(
            items=[Film(**item) for item in result.items],
            total=result.total,
        )
        return film_page

    async def search(self, query: str, page: int, size: int) -> Page[FilmBrief]:
        """Ищет фильмы по названию или описанию. Не кеширует результаты, так как вариантов может быть очень много."""
        params = SearchParams(
            query_fields=['title^3', 'description'],
            query_value=query,
            page_number=page,
            page_size=size,
        )
        search_results = await self.search_engine.search(table=self.table, params=params)

        film_page = Page(
            items=[FilmBrief(**item) for item in search_results.items],
            total=search_results.total,
            page=page,
            size=size,
        )
        return film_page

    async def get_sorted_filtered(
        self,
        sort: FilmSortingType,
        filter_field: FilmFilterType,
        filter_value: str,
        page: int,
        size: int,
    ) -> Page[FilmBrief]:
        """Возвращает список фильмов с фильтрацией и сортировкой."""
        params = SearchParams(
            sort_field=sort.value,
            filter_field=filter_field.value,
            filter_value=filter_value,
            page_number=page,
            page_size=size,
        )
        search_results = await self.search_engine.search(table=self.table, params=params)

        film_page = Page(
            items=[FilmBrief(**item) for item in search_results.items],
            total=search_results.total,
            page=page,
            size=size,
        )
        return film_page


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis), elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    search_engine = ElasticSearchEngine(elastic)
    return FilmService(redis, search_engine)
