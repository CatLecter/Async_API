import uuid
from typing import Dict, List, Optional, Union
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
