import json
from pathlib import Path
from typing import Dict


class ElasticHelper:
    def __init__(self, es_client):
        self.es_client = es_client

    async def create_index_from_file(self, index_name: str, file_path: str):
        """Создание индекса ElasticSearch из json-файла."""
        index_path = Path(file_path)
        with index_path.open(mode='r', encoding='utf-8') as json_file:
            index_body = json.load(json_file)
        await self.create_index(index_name, index_body)

    async def create_index(self, index_name: str, index_body: Dict):
        """Создание индекса ElasticSearch."""
        await self.es_client.indices.create(index=index_name, body=index_body, ignore=400)
