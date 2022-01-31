import json

import backoff
from config import log_config, storage
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException
from elasticsearch.helpers import bulk
from loguru import logger
from pymongo.errors import PyMongoError
from urllib3.exceptions import HTTPError
from utils import check_idx, mongo_conn_context

logger.add(**log_config)


class ElasticLoader:
    """Класс загрузки данных в Elasticsearch."""

    def __init__(
        self,
        es_host: str,
        mongo_host: str,
        prepared_collection: str,
        index_name: str,
        state: str,
    ):
        self.es_host = es_host
        self.mongo_host = mongo_host
        self.prepared_collection = prepared_collection
        self.index_name = index_name
        self.state = state

    @logger.catch
    @backoff.on_exception(backoff.expo, PyMongoError, 10)
    def get_bulk(self, prepared_collection: str) -> list:
        try:
            with mongo_conn_context(self.mongo_host) as mongo_client:
                db = mongo_client[storage]
                collection = db[prepared_collection]
                data = collection.find({}, {"_id": 0})
                return [_ for _ in data]
        except PyMongoError as e:
            logger.exception(e)

    @logger.catch
    @backoff.on_exception(backoff.expo, PyMongoError, 10)
    def update_state(self, list_id: list, state: str) -> None:
        try:
            with mongo_conn_context(self.mongo_host) as mongo_client:
                db = mongo_client[storage]
                collection = db[state]
                for _ in list_id:
                    collection.update_one(
                        {"id": str(_["id"])},
                        {"$set": {"need_load": False}},
                    )
        except PyMongoError as e:
            logger.exception(e)

    @logger.catch
    @backoff.on_exception(backoff.expo, PyMongoError, 10)
    def del_by_id(self, list_id: list, prepared_collection: str) -> None:
        """Удаление записей из коллекции с подготовленными
        данными, которые были загружены в Elasticsearch ранее.
        """

        try:
            with mongo_conn_context(self.mongo_host) as mongo_client:
                db = mongo_client[storage]
                collection = db[prepared_collection]
                for _ in list_id:
                    collection.delete_one({"id": str(_["id"])})
        except PyMongoError as e:
            logger.exception(e)

    @logger.catch
    @backoff.on_exception(backoff.expo, (ElasticsearchException, HTTPError), 10)
    def load(self, prepared_collection: str, index_name: str, state: str) -> None:
        """Загрузка данных в Elasticsearch."""

        prepared_bulk = self.get_bulk(prepared_collection)
        try:
            with Elasticsearch(hosts=self.es_host) as client:
                bulk(
                    client=client,
                    actions=[
                        {"_index": index_name, "_id": essence["id"], **essence}
                        for essence in prepared_bulk
                    ],
                )
            self.update_state(prepared_bulk, state)
            self.del_by_id(prepared_bulk, prepared_collection)
            logger.info(
                f"Данные из {prepared_collection} загружены в Elasticsearch, в индекс {index_name}"
            )
        except ElasticsearchException as e:
            logger.exception(e)
        finally:
            client.close()

    @logger.catch
    @backoff.on_exception(backoff.expo, (ElasticsearchException, HTTPError), 10)
    def create_index(self) -> None:
        """Проверка наличия файлов с индексами в папке indexes и
        создание соответствующих индексов в Elasticsearch, если таковые отсутствуют.
        """

        try:
            with Elasticsearch(hosts=self.es_host) as client:
                list_idx = check_idx()
                for idx in list_idx:
                    idx_name = idx.split(".")[0]
                    with open(f"indexes/{idx}", "r") as f:
                        _index = json.load(f)
                        client.indices.create(
                            index=idx_name,
                            body=_index,
                            ignore=400,
                        )
        except ElasticsearchException as e:
            logger.exception(e)
        finally:
            client.close()

    def __call__(self, *args, **kwargs):
        self.create_index()
        self.load(self.prepared_collection, self.index_name, self.state)
