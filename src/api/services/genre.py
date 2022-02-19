from typing import Optional

from engines.cache.general import CacheEngine
from engines.search.general import SearchEngine, SearchParams
from models.general import Page
from models.genre import Genre, GenreBrief


class GenreService:
    def __init__(self, cache_engine: CacheEngine, search_engine: SearchEngine):
        self.table = 'genres'
        self.cache_engine = cache_engine
        self.search_engine = search_engine

    async def get_by_uuid(self, uuid: str) -> Optional[Genre]:
        """Возвращает жанр по UUID."""
        cache_key = f'{self.table}:get_by_uuid(uuid={uuid})'

        data = await self.cache_engine.load_from_cache(cache_key)
        if not data:
            data = await self.search_engine.get_by_pk(table=self.table, pk=uuid)
            if not data:
                return None
            await self.cache_engine.save_to_cache(cache_key, data)

        return Genre(**data)

    async def search(
        self, query: str = None, page_number: int = None, page_size: int = None
    ) -> Page[GenreBrief]:
        """Ищет жанры по названию или описанию."""
        cache_key = f'{self.table}:search(query={query},page_number={page_number},page_size={page_size})'
        params = SearchParams()

        if page_number and page_size:
            params.page_number = page_number
            params.page_size = page_size

        if query:
            params.query_fields = ['name^5', 'description']
            params.query_value = query

        search_results = await self.cache_engine.load_from_cache(cache_key)
        if not search_results:
            search_results = await self.search_engine.search(table=self.table, params=params)
            await self.cache_engine.save_to_cache(cache_key, search_results)

        data_page = Page(
            items=[GenreBrief(**item) for item in search_results.items],
            total=search_results.total,
            page_number=page_number,
            page_size=page_size,
        )
        return data_page
