from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import NOT_FOUND_MESSAGE
from core.endpoints_params import *
from models.general import Page
from models.genre import Genre, GenreBrief
from services.genre import GenreService
from services.getters import get_genre_service

router = APIRouter(prefix='/genres', tags=['Жанры'])


@router.get(
    path='/{uuid}',
    name='Детали жанра',
    description='Получение детальной информации по жанру.',
    response_model=Genre,
)
async def genre_details(
    uuid: str = Query(**DEFAULT_UUID),
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_uuid(uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)
    return genre


@router.get(
    path='/',
    name='Список жанров',
    description='Список всех жанров на сайте.',
    response_model=Page[GenreBrief],
)
async def genre_list(
    query: str = Query(**DEFAULT_QUERY),
    genre_service: GenreService = Depends(get_genre_service),
) -> Page[GenreBrief]:
    page = await genre_service.search(query=query)
    return page
