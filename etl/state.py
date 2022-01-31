import json

import backoff
import psycopg2
from loguru import logger
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import PG_DSN, list_tables, log_config
from extractor import PsqlExtractor
from models import State

logger.add(**log_config)


class MongoState:
    """Класс работы с состоянием, хранимым в MondoDB"""

    def __init__(self, client: MongoClient, db: str):
        self.client = client
        self.db = self.client[db]
        self.names_table = list_tables

    @logger.catch
    @backoff.on_exception(backoff.expo, PyMongoError, 10)
    def get_id(self, _collection: str) -> tuple:
        """Получаем id записей, которые необходимо обновить, в виде кортежа."""

        collection = self.db[_collection]
        batch = collection.find({"need_load": True})
        result = []
        for row in batch:
            result.append(row["id"])
        return tuple(result)

    def additional_verification(self):
        """Дополнительная проверка фильмов по обновлению жанров и персон."""

        pass

    @logger.catch
    @backoff.on_exception(backoff.expo, OperationalError, 10)
    def update_state(
        self, pg: PsqlExtractor, name_table: str, _collection: str
    ) -> None:
        """
        Анализ записей в Postgres и, при необходимости
        обновление state в MongoDB storage.
        """
        # обращаемся к коллекции
        collection = self.db[_collection]
        # получаем id, updated_at из таблицы в PostgreSQL
        data = (_ for _ in pg.get_table(name_table))
        while True:
            try:
                value = next(data)
                # валидируем данные через pydantic модель
                essence = State(**value)
                # проверяем есть ли в коллекции MongoDB такая запись
                find_id = collection.find_one({"id": str(essence.id)})
                if find_id is None:
                    as_json = json.loads(essence.json())
                    # если такой записи нет, то добавляем её в коллекцию
                    collection.insert_one(as_json)
                    logger.info(f"В {_collection} добавлена запись с id: {essence.id}.")
                elif str(essence.updated_at) > find_id["updated_at"]:
                    # если такая запись есть в коллекции и она более новая, то обновляем её
                    collection.update_one(
                        {"id": str(essence.id)},
                        {
                            "$set": {
                                "updated_at": str(essence.updated_at),
                                "need_load": True,
                            }
                        },
                    )
                    logger.info(f"В {_collection} обновлена запись с id: {essence.id}.")
            except StopIteration:
                break

    def __call__(self, *args, **kwargs):
        try:
            with psycopg2.connect(**PG_DSN, cursor_factory=DictCursor) as pg_conn:
                pg = PsqlExtractor(pg_conn=pg_conn)
                for table in self.names_table:
                    name_collection = table
                    self.update_state(pg, table, name_collection)
        except OperationalError as e:
            logger.exception(e)
        finally:
            pg_conn.close()
