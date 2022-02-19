from typing import Optional

from engines.cache.general import CacheEngine
from engines.search.general import SearchEngine, SearchParams
from models.general import Page
from models.person import Person, PersonBrief


class PersonService:
    def __init__(self, cache_engine: CacheEngine, search_engine: SearchEngine):
        self.table = 'persons'
        self.cache_engine = cache_engine
        self.search_engine = search_engine

    async def get_by_uuid(self, uuid: str) -> Optional[Person]:
        """Возвращает персону по UUID."""
        cache_key = f'{self.table}:get_by_uuid(uuid={uuid})'

        data = await self.cache_engine.load_from_cache(cache_key)
        if not data:
            data = await self.search_engine.get_by_pk(table=self.table, pk=uuid)
            if not data:
                return None
            await self.cache_engine.save_to_cache(cache_key, data)

        return Person(**data)

    async def search(self, query: str, page_number: int, page_size: int) -> Page[PersonBrief]:
        """Ищет персон по имени. Не кеширует результаты, так как вариантов может быть очень много."""
        params = SearchParams(
            query_fields=['full_name'],
            query_value=query,
            page_number=page_number,
            page_size=page_size,
        )

        search_results = await self.search_engine.search(table=self.table, params=params)

        data_page = Page(
            items=[PersonBrief(**item) for item in search_results.items],
            total=search_results.total,
            page_number=page_number,
            page_size=page_size,
        )
        return data_page
