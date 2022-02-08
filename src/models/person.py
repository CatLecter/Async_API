from typing import List, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Id(BaseModel):
    id: str


class Film(Id):
    title: Optional[str]
    imdb_rating: Optional[float]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(Id):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[List[Film]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
