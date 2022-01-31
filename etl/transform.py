import json
from typing import Generator

import backoff
from loguru import logger
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from config import MONGO_URI, log_config, storage
from utils import mongo_conn_context

logger.add(**log_config)


class Transform:
    def __init__(self, raw_data: Generator, model, collection_name: str):
        self.raw_data = raw_data
        self.collect_name = collection_name
        self.transform_model = model

    @logger.catch
    @backoff.on_exception(backoff.expo, PyMongoError, 10)
    def record_data(self) -> None:
        """Запись в соответствующую коллекцию подготовленных данных."""

        try:
            with mongo_conn_context(MONGO_URI) as mongo_client:
                db = mongo_client[storage]
                # обращаемся к коллекции с подготовленными данными
                collection = db[self.collect_name]
                while True:
                    try:
                        value = next(self.raw_data)
                        try:
                            # валидируем данные через pydantic модель
                            data_for_index = self.transform_model(**value)
                            # проверяем наличие записи в подготовленных данных
                            find_id = collection.find_one(
                                {"id": str(data_for_index.id)}
                            )
                            # если такой записи нет
                            if find_id is None:
                                as_json = json.loads(data_for_index.json())
                                # то записываем её к подготовленным данным
                                collection.insert_one(as_json)
                                logger.info(
                                    f"Запись с id: {data_for_index.id} обработана и отправлена в {self.collect_name}."
                                )
                        except ValidationError as err:
                            logger.exception(err)
                    except StopIteration:
                        break
        except Exception as e:
            logger.exception(e)

    def __call__(self, *args, **kwargs):
        self.record_data()
