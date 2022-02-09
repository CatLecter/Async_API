import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_loader import SQLiteLoader

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    data = sqlite_loader.get_all_data()
    postgres_saver.save_all_data(data)


if __name__ == "__main__":
    dsl = {
        "dbname": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "host": os.environ.get("POSTGRES_HOST"),
        "port": os.environ.get("POSTGRES_PORT"),
        "options": "-c search_path=content",
    }
    try:
        with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(
            **dsl, cursor_factory=DictCursor
        ) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except (psycopg2.OperationalError, sqlite3.OperationalError) as e:
        print("Error:", e)
    finally:
        pg_conn.close()
        sqlite_conn.close()
