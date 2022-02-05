from http import HTTPStatus
from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]


# заголовок, содержание, дата создания, возрастной ценз, режиссёры, актёры, сценаристы, жанры, ссылка на файл.
class Film(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    # # дата создания
    # # возрастной ценз
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    actors: Optional[List[Dict[str, str]]]
    writers_names: Optional[List[str]]
    genre: Optional[List[Optional[Genre]]]
    # ссылка на файл.


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get("/{film_id}", response_model=Film)
async def film_details(
        film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
        # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
    # Которое отсутствует в модели ответа API.
    # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
    # вы бы предоставляли клиентам данные, которые им не нужны
    # и, возможно, данные, которые опасно возвращать
    return Film(id=film.id,
                title=film.title,
                description=film.description,
                director=film.director,
                actors=film.actors,
                actors_names=film.actors_names,
                writers_names=film.writers_names,
                genre=film.genre
                )
