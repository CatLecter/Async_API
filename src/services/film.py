from collections import defaultdict
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from db.elastic import get_elastic
from db.redis import get_redis
from models.base import orjson_dumps, orjson_loads
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def get_films_list(self, search_params: Optional[dict]) -> list[Film]:
        def change_sort_order(srt):
            value = "asc"
            if srt.startswith("-"):
                srt = srt.removeprefix("-")
                value = "desc"
            return srt, value

        def body_with_filter(filter_by, type_, type_id):
            out = {
                "bool": {
                    "filter": {
                        "nested": {
                            "path": type_,
                            "query": {
                                "bool": {"filter": {"term": {type_id: filter_by}}}
                            },
                        }
                    }
                }
            }
            return out

        sort = search_params["sort"]
        page_size = search_params["page_size"]
        page_number = search_params["page_number"]
        filter_genre = search_params["filter_genre"]
        sort, order_value = change_sort_order(sort)
        body = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "sort": {sort: {"order": order_value}},
        }
        if filter_genre:
            body["query"] = body_with_filter(filter_genre, "genre", "genre.id")

        redis_key = await self._generate_radis_key(
            sort, order_value, filter_genre, page_size, page_number
        )
        data = await self._get_data_from_cache(redis_key)
        if not data:
            data = await self.elastic.search(index="movies", body=body)
            await self._put_data_to_cache(redis_key, None, data)

        items = map(
            lambda item: {"id": item["_id"], **item["_source"]},
            data.get("hits", {}).get("hits", []),
        )
        return parse_obj_as(list[Film], list(items))

    async def search_films(self, search_params: Optional[dict]):
        query = search_params["query"]
        page_size = search_params["page_size"]
        page_number = search_params["page_number"]
        body = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "query": {
                "simple_query_string": {
                    "query": query,
                    "fields": ["title", "description"],
                    "default_operator": "or",
                }
            },
        }
        data = await self.elastic.search(index="movies", body=body)
        items = map(
            lambda item: {"id": item["_id"], **item["_source"]},
            data.get("hits", {}).get("hits", []),
        )
        return parse_obj_as(list[Film], list(items))

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get("movies", film_id)
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _generate_radis_key(self, *args):
        """формируем уникальное значение hash, состоящее из строки параметров запроса
        и используем его как ключ к redis"""
        args_str = "_".join([str(arg) for arg in args])
        return str(hash(f"{args_str}"))

    async def _put_data_to_cache(self, redis_key, default, data):
        await self.redis.set(
            redis_key,
            orjson_dumps(data, default=default),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS,
        )

    async def _get_data_from_cache(self, redis_key):
        data = await self.redis.get(redis_key)
        if not data:
            return None
        data = orjson_loads(data.decode("utf8"))
        return data


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
