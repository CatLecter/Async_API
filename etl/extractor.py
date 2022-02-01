import backoff
from psycopg2 import OperationalError
from psycopg2.extensions import connection


class PsqlExtractor:
    """Класс для выгрузки данных из PostgreSQL."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, 10)
    def get_table(self, table_name):
        self.cursor.execute(
            f"""
            SELECT id, updated_at
            FROM content.{table_name}
            ORDER BY updated_at
            """
        )
        return self.cursor.fetchall()

    def get_persons_id(self, tuple_id: tuple):
        self.cursor.execute(
            f"""
            SELECT film_work.id AS film_work_id FROM content.film_work
            LEFT JOIN content.person_film_work ON (person_film_work.film_work_id = film_work.id)
            WHERE person_film_work.person_id IN {tuple_id}
            """
        )
        return self.cursor.fetchall()

    def get_genres_id(self, tuple_id: tuple):
        self.cursor.execute(
            f"""
            SELECT film_work.id AS film_work_id FROM content.film_work
            LEFT JOIN content.genre_film_work ON (genre_film_work.film_work_id = film_work.id)
            WHERE genre_film_work.genre_id IN {tuple_id}
            """
        )
        return self.cursor.fetchall()

    def get_genre_by_id(self, tuple_id: tuple):
        self.cursor.execute(
            f"""
            SELECT genre.id,
                   genre.name,
                   genre.description,
                   JSON_AGG(DISTINCT jsonb_build_object('id', film_work.id, 'title', film_work.title, 'imdb_rating', film_work.rating)) AS films
            FROM content.genre
                LEFT OUTER JOIN content.genre_film_work ON (genre.id = genre_film_work.genre_id)
                LEFT OUTER JOIN content.film_work ON (genre_film_work.film_work_id = film_work.id)
            WHERE genre.id IN {tuple_id}
            GROUP BY genre.id, genre.name
            """
        )
        return self.cursor.fetchall()

    def get_person_by_id(self, tuple_id: tuple):
        self.cursor.execute(
            f"""
            SELECT
                person.id,
                person.full_name,
                person_film_work.role,
                JSON_AGG(DISTINCT jsonb_build_object('id', person_film_work.film_work_id)) AS film_ids
            FROM content.person
                LEFT OUTER JOIN content.person_film_work ON (person.id = person_film_work.person_id)
            WHERE person.id IN {tuple_id}
            GROUP BY person.id, person.full_name, person_film_work.role;
            """
        )
        return self.cursor.fetchall()

    def get_films_by_id(self, tuple_id: tuple):
        self.cursor.execute(
            f"""
            SELECT
                film_work.id,
                film_work.rating AS imdb_rating,
                film_work.title,
                film_work.description,
                JSON_AGG(DISTINCT jsonb_build_object('id', genre.id, 'name', genre.name)) AS genre,
                JSON_AGG(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'director') AS director,
                JSON_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
                    FILTER (WHERE person_film_work.role = 'actor') AS actors,
                JSON_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name))
                    FILTER (WHERE person_film_work.role = 'writer') AS writers,
                ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'actor') AS actors_names,
                ARRAY_AGG(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'writer') AS writers_names
            FROM content.film_work
                LEFT OUTER JOIN content.genre_film_work ON (film_work.id = genre_film_work.film_work_id)
                LEFT OUTER JOIN content.genre ON (genre_film_work.genre_id = genre.id)
                LEFT OUTER JOIN content.person_film_work ON (film_work.id = person_film_work.film_work_id)
                LEFT OUTER JOIN content.person ON (person_film_work.person_id = person.id)
            WHERE film_work.id IN {tuple_id}
            GROUP BY film_work.id, film_work.title, film_work.description, film_work.rating
            """
        )
        return self.cursor.fetchall()
