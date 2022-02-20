import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import api
from core import config
from db.elastic import elastic_connect, elastic_disconnect
from db.redis import redis_connect, redis_disconnect

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    license_info=config.PROJECT_LICENSE_INFO,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    openapi_tags=config.PROJECT_TAGS_METADATA,
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    await asyncio.gather(
        redis_connect(), elastic_connect(),
    )


@app.on_event('shutdown')
async def shutdown():
    await asyncio.gather(
        redis_disconnect(), elastic_disconnect(),
    )


app.include_router(api.router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000,
    )
