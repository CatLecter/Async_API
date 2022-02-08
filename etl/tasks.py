import psycopg2
from celery import Celery, chain
from celery.schedules import crontab
from config import BROKER_URL, ES_URI, MONGO_URI, PG_DSN, log_config, storage
from extractor import PsqlExtractor
from loader import ElasticLoader
from loguru import logger
from psycopg2 import DatabaseError, OperationalError
from psycopg2.extras import DictCursor
from pymongo.errors import PyMongoError
from state import MongoState
from transform import Transform
from utils import mongo_conn_context

from models import Films, Genres, Persons

logger.add(**log_config)

celery_app = Celery("tasks", broker=BROKER_URL)


@celery_app.task
def serve_state() -> bool:
    """Задача для обслуживания состояния, хронящегося в MondoDB."""

    try:
        with mongo_conn_context(MONGO_URI) as mongo_client:
            serve = MongoState(mongo_client, storage)
            serve()
    except PyMongoError as e:
        logger.exception(e)
    return True


@celery_app.task
def transform_genres(previous_task: bool) -> bool:
    """Задача трансформации и сохранения в MongoDB жанров, требующих обновления."""

    if previous_task:
        try:
            with mongo_conn_context(MONGO_URI) as mongo_client, psycopg2.connect(
                **PG_DSN, cursor_factory=DictCursor
            ) as pg_conn:
                pg = PsqlExtractor(pg_conn)
                serve = MongoState(mongo_client, storage)
                # получаем id жанров, которые нуждаются в обновлении
                genres_id = serve.get_id("genre")
                if genres_id:
                    # получаем сырые данные жанров
                    raw_data = (_ for _ in pg.get_genre_by_id(genres_id))
                    # и передаём их на обработку
                    make_transform = Transform(raw_data, Genres, "prepared_genres")
                    make_transform()
                else:
                    logger.info("Нечего обновлять")
        except (OperationalError, DatabaseError, PyMongoError) as e:
            logger.exception(e)
        return True


@celery_app.task
def transform_persons(previous_task: bool) -> bool:
    """Задача трансформации и сохранения в MongoDB персон, требующих обновления."""

    if previous_task:
        try:
            with mongo_conn_context(MONGO_URI) as mongo_client, psycopg2.connect(
                **PG_DSN, cursor_factory=DictCursor
            ) as pg_conn:
                pg = PsqlExtractor(pg_conn)
                serve = MongoState(mongo_client, storage)
                # получаем id персон, которые нуждаются в обновлении
                person_id = serve.get_id("person")
                if person_id:
                    # получаем сырые данные персон
                    raw_data = (_ for _ in pg.get_person_by_id(person_id))
                    # и передаём их на обработку
                    make_transform = Transform(raw_data, Persons, "prepared_persons")
                    make_transform()
                else:
                    logger.info("Нечего обновлять")
        except (OperationalError, DatabaseError, PyMongoError) as e:
            logger.exception(e)
        return True


@celery_app.task
def transform_films_work(previous_task: bool) -> bool:
    """Задача трансформации и сохранения в MongoDB фильмов, требующих обновления."""

    if previous_task:
        try:
            with mongo_conn_context(MONGO_URI) as mongo_client, psycopg2.connect(
                **PG_DSN, cursor_factory=DictCursor
            ) as pg_conn:
                pg = PsqlExtractor(pg_conn)
                serve = MongoState(mongo_client, storage)
                # получаем id жанров, которые нуждаются в обновлении
                film_id = serve.get_id("film_work")
                if film_id:
                    # получаем сырые данные фильмов
                    raw_data = (_ for _ in pg.get_films_by_id(film_id))
                    # и передаём их на обработку
                    make_transform = Transform(raw_data, Films, "prepared_film_work")
                    make_transform()
                else:
                    logger.info("Нечего обновлять")
        except (OperationalError, DatabaseError, PyMongoError) as e:
            logger.exception(e)
        return True


@celery_app.task
def es_load(previous_task: bool) -> None:
    """Задача загрузки подготовленных данных в Elacticsearch."""

    if previous_task:
        genres_load = ElasticLoader(
            es_host=ES_URI,
            mongo_host=MONGO_URI,
            prepared_collection="prepared_genres",
            index_name="genres",
            state="genre",
        )
        genres_load()
        persons_load = ElasticLoader(
            es_host=ES_URI,
            mongo_host=MONGO_URI,
            prepared_collection="prepared_persons",
            index_name="persons",
            state="person",
        )
        persons_load()
        films_load = ElasticLoader(
            es_host=ES_URI,
            mongo_host=MONGO_URI,
            prepared_collection="prepared_film_work",
            index_name="movies",
            state="film_work",
        )
        films_load()


@celery_app.task
def etl() -> None:
    """Последовательно выполняемые задачи."""

    chain(
        serve_state.s(),
        transform_genres.s(),
        transform_persons.s(),
        transform_films_work.s(),
        es_load.s(),
    ).delay()


@celery_app.on_after_configure.connect
def setup_periodic_taskc(sender, **kwargs):
    """Планировщик запуска ETL (раз в 1 минуту)."""

    sender.add_periodic_task(crontab(minute="*/1"), etl.s())