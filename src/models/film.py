from typing import Dict, List, Optional

from models.base import Base


class Genre(Base):
    name: Optional[str]


class Film(Base):
    imdb_rating: Optional[float]
    genre: Optional[List[Optional[Genre]]]
    title: Optional[str]
    description: Optional[str]
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]
