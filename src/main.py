import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film
from core import config
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/film
# Теги указываем для удобства навигации по документации
app.include_router(film.router, prefix="/api/v1/film", tags=["film"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
