from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

ResultType = TypeVar('ResultType')


class SearchResult(BaseModel, Generic[ResultType]):
    """Ответ поискового движка."""
    items: List[ResultType]
    total: int
    page_number: int
    page_size: int


class SearchParams(BaseModel):
    """Параметры поискового запроса."""
    query: Optional[str]
    sort: Optional[str]
    filter_type: Optional[str]
    filter_value: Optional[str]
    page_number: int = 1
    page_size: int = 10


class SearchEngine(ABC):
    """Класс абстрактного поискового движка."""

    @abstractmethod
    def get_by_uuid(self, table: str, uuid: str) -> SearchResult:
        """Возвращает объект по UUID."""
        pass

    @abstractmethod
    def search(self, table: str, params: SearchParams) -> SearchResult:
        """Возвращает объекты подходящие под параметры поиска."""
        pass
