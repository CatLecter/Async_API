from cache_engine.general import AbstractCache


class DummyCache(AbstractCache):
    async def save_to_cache(self, cache_key, data) -> None:
        pass

    async def load_from_cache(self, cache_key) -> None:
        return None
