import json

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import config


class ESHelper:
    def __init__(self) -> None:
        self.client = AsyncElasticsearch(hosts=f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}")

    def get_client(self) -> AsyncElasticsearch:
        return self.client

    async def create_index(self, name_index: str, file_index: str):
        async with open(f"testdata/{file_index}.json", "r", encoding="utf-8") as f:
            index_data = json.load(f)
            await self.client.indices.create(index=name_index, body=index_data, ignore=400)

    async def delete_index(self, name_index: str):
        await self.client.indices.delete(index=name_index, ignore=[400, 404])
