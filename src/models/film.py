import uuid
from typing import Dict, List, Optional, Union

import orjson
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    id: Union[int, str, uuid.UUID]
    imdb_rating: Optional[float]
    genre: List[str]
    title: str
    description: Optional[str]
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Dict[str, str]]
    writers: List[Dict[str, str]]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# class TvSeries(Film):
#     pass


class Genre(BaseModel):
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[list]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# class Actor(Person):
#     pass
#
# class Director(Person):
#     pass
#
# class Writer(Person):
#     pass
