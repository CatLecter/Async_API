from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class Id(BaseModel):
    id: UUID


class State(Id):
    updated_at: datetime
    need_load: Optional[bool] = True


class Films(Id):
    imdb_rating: Optional[float]
    title: Optional[str]
    description: Optional[str]
    genre: Optional[list]
    director: Optional[list]
    actors: Optional[List[dict]]
    writers: Optional[List[dict]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]


class Genres(Id):
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]


class Persons(Id):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[List[Id]]
