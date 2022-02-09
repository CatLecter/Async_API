from typing import Dict, List, Optional

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel

from models.base import Base


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]


class Film(Base):
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
