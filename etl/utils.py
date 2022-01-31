import os
from contextlib import contextmanager

from pymongo import MongoClient


@contextmanager
def mongo_conn_context(mongo_uri: str):
    mongo_client = MongoClient(mongo_uri)
    yield mongo_client
    mongo_client.close()


def list_to_tuple(list_id: list) -> tuple:
    return tuple([str(*_) for _ in list_id])


def check_idx():
    files = os.walk("indexes")
    list_idx = []
    for idx in files:
        list_idx = idx[2]
    return list_idx
