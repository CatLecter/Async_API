import os

from dotenv import load_dotenv

load_dotenv()


PG_DSN = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": "postgres",
    "port": os.environ.get("POSTGRES_PORT"),
    "options": "-c search_path=content",
}

storage = "storage"

list_tables = ["film_work", "genre", "person"]

mongo_user = os.environ.get("MONGO_USER")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_host = os.environ.get("MONGO_HOST")
mongo_port = os.environ.get("MONGO_PORT")
MONGO_URI = os.environ.get("MONGO_URL")

BROKER_URL = os.environ.get("BROKER_URL")

es_host = os.environ.get("ELASTIC_HOST")
es_port = os.environ.get("ELASTIC_PORT")

ES_URI = f"{es_host}:{es_port}"

log_config = {
    "sink": "./log/etl.log",
    "format": "{time} {level} {message}",
    "level": "INFO",
    "rotation": "00:00",
    "compression": "zip",
}