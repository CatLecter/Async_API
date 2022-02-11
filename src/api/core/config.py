import os
from datetime import timedelta
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Настройки проекта.
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')
NOT_FOUND_MESSAGE = 'object not found'

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
CACHE_TTL = timedelta(minutes=5)

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elastic')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
