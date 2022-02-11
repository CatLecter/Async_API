from typing import Generic, List, TypeVar

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


PT = TypeVar('PT')


class Page(FastJsonModel, Generic[PT]):
    """Страница результатов с пагинацией."""

    items: List[PT] = Field(
        default=[], title='Список объектов',
    )

    total: int = Field(
        title='Всего объектов', default=0, example=35,
    )
    page: int = Field(
        title='Номер страницы', default=1, example=1,
    )
    size: int = Field(
        title='Объектов на странице', default=20, example=20,
    )
