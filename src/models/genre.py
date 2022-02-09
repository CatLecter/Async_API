from typing import List, Optional

import orjson

from models.base import Base


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(Base):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]
