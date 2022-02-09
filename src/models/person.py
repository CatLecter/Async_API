from typing import List, Optional

import orjson

from models.base import Base


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Id(Base):
    id: str


class Film(Id):
    title: Optional[str]
    imdb_rating: Optional[float]


class Person(Id):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[List[Film]]
