from abc import ABC, abstractmethod
from typing import Any


class AbstractCache(ABC):
    """
    Абстрактный класс для кэширования
    """

    @abstractmethod
    async def save_to_cache(self, cache_key: str, data: Any) -> None:
        """Сохраняет в кэш."""
        pass

    @abstractmethod
    async def load_from_cache(self, cache_key: str) -> Any:
        """Загружает из кэша."""
        pass
