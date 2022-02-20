from typing import Optional

from engines.cache.general import CacheEngine
from engines.search.general import SearchEngine, SearchParams
from models.film import Film, FilmBrief, FilmFilterType, FilmSortingType
from models.general import Page


class FilmService:
    def __init__(self, cache_engine: CacheEngine, search_engine: SearchEngine):
        self.table = 'movies'
        self.cache_engine = cache_engine
        self.search_engine = search_engine

    async def get_by_uuid(self, uuid: str) -> Optional[Film]:
        """Возвращает фильм по UUID."""
        cache_key = f'{self.table}:get_by_uuid(uuid={uuid})'

        data = await self.cache_engine.load_from_cache(cache_key)
        if not data:
            data = await self.search_engine.get_by_pk(table=self.table, pk=uuid)
            if not data:
                return None
            await self.cache_engine.save_to_cache(cache_key, data)

        return Film(**data)

    async def search(self, query: str, page_number: int, page_size: int) -> Page[FilmBrief]:
        """Ищет фильмы по названию или описанию. Не кеширует результаты, так как вариантов может быть очень много."""
        params = SearchParams(
            query_fields=['title^3', 'description'],
            query_value=query,
            page_number=page_number,
            page_size=page_size,
        )

        search_results = await self.search_engine.search(table=self.table, params=params)

        data_page = Page(
            items=[FilmBrief(**item) for item in search_results.items],
            total=search_results.total,
            page_number=page_number,
            page_size=page_size,
        )
        return data_page

    async def get_sorted_filtered(
        self,
        sort: FilmSortingType,
        filter_field: FilmFilterType,
        filter_value: str,
        page_number: int,
        page_size: int,
    ) -> Page[FilmBrief]:
        """Возвращает список фильмов с фильтрацией и сортировкой."""
        cache_key = f'{self.table}:get_sorted_filtered(sort={sort.value},filter_field={filter_field.value},filter_value={filter_value},page_number={page_number},page_size={page_size}))'
        params = SearchParams(
            sort_field=sort.value,
            filter_field=filter_field.value,
            filter_value=filter_value,
            page_number=page_number,
            page_size=page_size,
        )

        search_results = await self.cache_engine.load_from_cache(cache_key)
        if not search_results:
            search_results = await self.search_engine.search(table=self.table, params=params)
            await self.cache_engine.save_to_cache(cache_key, search_results)

        data_page = Page(
            items=[FilmBrief(**item) for item in search_results.items],
            total=search_results.total,
            page_number=page_number,
            page_size=page_size,
        )
        return data_page
