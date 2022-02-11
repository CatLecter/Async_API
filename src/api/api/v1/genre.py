from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import NOT_FOUND_MESSAGE
from models.genre import Genre, GenreBrief
from services.genre import GenreService, get_genre_service

router = APIRouter(prefix='/genre', tags=['genre'])


@router.get(
    path='/{genre_uuid}',
    name='Детали жанра',
    description='Получение детальной информации по жанру.',
    response_model=Genre,
)
async def genre_details(
    genre_uuid: str = Query(
        title='UUID жанра',
        default=None,
        description='Поиск жанра по его UUID.',
        example='2f89e116-4827-4ff4-853c-b6e058f71e31',
    ),
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_uuid(genre_uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)
    return genre


@router.get(
    path='/',
    name='Список жанров',
    description='Список всех жанров на сайте.',
    response_model=List[GenreBrief],
)
async def genre_list(
    genre_service: GenreService = Depends(get_genre_service),
) -> List[GenreBrief]:
    page = await genre_service.genre_list()
    return page
