from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from core.config import Settings
from services.film import FilmService, get_film_service

router = APIRouter()

settings = Settings()


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]


# заголовок, содержание, дата создания, возрастной ценз, режиссёры, актёры, сценаристы, жанры, ссылка на файл.
class Film(BaseModel):
    id: Optional[str]
    title: Optional[str]
    imdb_rating: Optional[float]


class FullFilm(Film):
    description: Optional[str]
    # # дата создания
    # # возрастной ценз
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    actors: Optional[List[Dict[str, str]]]
    writers_names: Optional[List[str]]
    genre: Optional[List[Optional[Genre]]]
    # ссылка на файл.


@router.get(
    "",
    response_model=list[Film],
    summary="Список фильмов",
    description="Информация о фильмах + сортировка по imdb_rating + фильтр по uuid жанров",
)
async def films_list(
    sort_: Optional[str] = Query("-imdb_rating", alias="sort"),
    page_size_: Optional[int] = Query(50, alias="page[size]"),
    page_number_: Optional[int] = Query(1, alias="page[number]"),
    filter_genre_: Optional[UUID] = Query(None, alias="filter[genre]"),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    search_params = {
        "sort": sort_,
        "page_size": page_size_,
        "page_number": page_number_,
        "filter_genre": filter_genre_,
    }
    films = await film_service.get_films_list(search_params=search_params)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.FILMS_NOT_FOUND
        )
    films = [Film(**f.dict()) for f in films]
    return films


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/{film_id}",
    response_model=FullFilm,
    summary="Полная информация по фильму",
    description="Фильм отображается по uuid",
)
async def film_details(
    film_id: str = Query(
        title="UUID фильма",
        default=None,
        example="120b091b-c266-41e9-9be6-64e6751c02ad",
    ),
    film_service: FilmService = Depends(get_film_service),
) -> FullFilm:
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
        # Такой код будет более поддерживаемым
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.FILMS_NOT_FOUND
        )

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
    # Которое отсутствует в модели ответа API.
    # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
    # вы бы предоставляли клиентам данные, которые им не нужны
    # и, возможно, данные, которые опасно возвращать
    return FullFilm(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        director=film.director,
        actors=film.actors,
        actors_names=film.actors_names,
        writers_names=film.writers_names,
        genre=film.genre,
    )


@router.get(
    "/search/",
    response_model=list[Film],
    summary="Поиск фильмов",
    description="Поиск фильмов по заголовку и/или описанию.",
)
async def search_films(
    query_: Optional[str] = Query(default=None, example="Captain", alias="query"),
    page_size_: Optional[int] = Query(50, alias="page[size]"),
    page_number_: Optional[int] = Query(1, alias="page[number]"),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    search_params = {
        "query": query_,
        "page_size": page_size_,
        "page_number": page_number_,
    }
    films = await film_service.search_films(search_params=search_params)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.FILMS_NOT_FOUND
        )
    films = [Film(**f.dict()) for f in films]
    return films
