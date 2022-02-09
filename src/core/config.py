import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

    # Настройки Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # Настройки Elasticsearch
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
    ELASTIC_PORT: int = int(os.getenv("ELASTIC_PORT", 9200))

    # Корень проекта
    BASE_DIR: str = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    class Config:
        env_file = '.env'
