import json

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import bulk

from tests.functional.settings import config
from tests.functional.utils.utils import names_file


class ESHelper:
    def __init__(self) -> None:
        self.client = AsyncElasticsearch(
            hosts=f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"
        )

    async def create_index(self):
        """Метод создаёт индексы, лежащие в папке testdata/indexes.
        Наименование индекса в Elasticsearch совпадает с именем файла.
        """

        for index in names_file("../testdata/indexes"):
            with open(f"../testdata/indexes/{index}.json", "r") as f:
                index_data = json.load(f)
            await self.client.indices.create(index=index, body=index_data, ignore=400)

    async def load_data(self):
        """Метод загружает данные лежащие в папке
        testdata/data_for_indexes в индексы.
        Имена файлов должны соответствовать имени индекса.
        """

        """НЕ ТЕСТИРОВАЛСЯ"""
        for name in names_file("../testdata/data_for_indexes"):
            with open(f"../testdata/data_for_indexes/{name}.json", "r") as f:
                index_data = json.load(f)
            await bulk(
                client=self.client,
                actions=[
                    {"_index": name, "_id": essence["id"], **essence}
                    for essence in index_data
                ],
            )

    async def delete_index(self):
        for index in check_idx():
            await self.client.indices.delete(index=index, ignore=[400, 404])
