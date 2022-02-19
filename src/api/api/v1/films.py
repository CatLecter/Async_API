from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import NOT_FOUND_MESSAGE
from models.film import Film, FilmBrief, FilmFilterType, FilmSortingType
from models.general import Page
from services.film import FilmService
from services.getters import get_film_service

router = APIRouter(prefix='/films', tags=['Фильмы'])


@router.get(
    path='/{uuid}',
    name='Детали фильма',
    description='Получение детальной информации по фильму.',
    response_model=Film,
)
async def film_details(
    uuid: str = Query(
        title='UUID фильма',
        default=None,
        description='Поиск фильма по его UUID.',
        example='4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f',
    ),
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    result = await film_service.get_by_uuid(uuid)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)
    return result


@router.get(
    path='/search/',
    name='Поиск фильмов',
    description='Поиск фильмов по заголовку или описанию.',
    response_model=Page[FilmBrief],
)
async def film_search(
    query: str = Query(
        title='Поиск', default=None, description='Поиск по тексту.', example='Captain',
    ),
    page_number: Optional[int] = Query(
        alias='page[number]', title='Страница', default=1, ge=1, description='Номер страницы.',
    ),
    page_size: Optional[int] = Query(
        alias='page[size]',
        title='Размер',
        default=20,
        ge=1,
        le=100,
        description='Результатов на странице.',
    ),
    film_service: FilmService = Depends(get_film_service),
) -> Page[FilmBrief]:
    page = await film_service.search(query, page_number, page_size)
    return page


@router.get(
    path='/',
    name='Сортировка и фильтрация фильмов',
    description='Список фильмов по заданным критериям сортировки и фильтрации.',
    response_model=Page[FilmBrief],
)
async def film_list(
    sort: Optional[FilmSortingType] = Query(
        title='Сортировка',
        default=None,
        description='Критерий сортировки.',
        example=FilmSortingType.imdb_rating_desc,
    ),
    filter_type: Optional[FilmFilterType] = Query(
        default=None,
        title='Тип фильтрации',
        description='Выберите тип фильтрации из предложенных.',
        example='genres',
    ),
    filter_value: Optional[str] = Query(
        default=None,
        title='Значение для фильтрации',
        description='UUID для сортировки по выбранному типу.',
        example='0b105f87-e0a5-45dc-8ce7-f8632088f390',
    ),
    page_number: Optional[int] = Query(
        alias='page[number]', title='Страница', default=1, ge=1, description='Номер страницы.',
    ),
    page_size: Optional[int] = Query(
        alias='page[size]',
        title='Размер',
        default=20,
        ge=1,
        le=100,
        description='Результатов на странице.',
    ),
    film_service: FilmService = Depends(get_film_service),
) -> Page[FilmBrief]:
    page = await film_service.get_sorted_filtered(
        sort, filter_type, filter_value, page_number, page_size
    )
    return page
