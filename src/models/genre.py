from typing import List, Optional

from models.base import Base


class Genre(Base):
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]
