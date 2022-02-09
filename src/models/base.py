import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def orjson_loads(bytes_obj):
    return orjson.loads(bytes_obj)


class Base(BaseModel):
    id: str

    class Config:
        json_loads = orjson_loads
        json_dumps = orjson_dumps
