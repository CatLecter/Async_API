import uuid
from typing import Dict, List, Optional, Union

import orjson
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]


class Film(BaseModel):
    id: Optional[str]
    imdb_rating: Optional[float]
    genre: Optional[List[Optional[Genre]]]
    title: Optional[str]
    description: Optional[str]
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
