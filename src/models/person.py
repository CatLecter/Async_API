from typing import List, Optional

from models.base import Base


class Film(Base):
    title: Optional[str]
    imdb_rating: Optional[float]


class Person(Base):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[List[Film]]
