from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import NOT_FOUND_MESSAGE
from models.general import Page
from models.person import Person, PersonBrief
from services.person import PersonService, get_person_service

router = APIRouter(prefix='/persons', tags=['Персоны'])


@router.get(
    path='/{person_uuid}',
    name='Детали персоны',
    description='Получение детальной информации по персоне.',
    response_model=Person,
)
async def person_details(
    person_uuid: str = Query(
        title='UUID фильма',
        default=None,
        description='Поиск фильма по его UUID.',
        example='4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f',
    ),
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_uuid(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)
    return person


@router.get(
    path='/search/',
    name='Поиск персон',
    description='Поиск персон по имени.',
    response_model=Page[PersonBrief],
)
async def person_search(
    query: str = Query(
        title='Поиск', default=None, description='Поиск по тексту.', example='Captain',
    ),
    page: Optional[int] = Query(
        alias='page[number]', title='Страница', default=1, ge=1, description='Номер страницы.',
    ),
    size: Optional[int] = Query(
        alias='page[size]',
        title='Размер',
        default=20,
        ge=1,
        le=50,
        description='Результатов на странице.',
    ),
    person_service: PersonService = Depends(get_person_service),
) -> Page[PersonBrief]:
    page = await person_service.get_search_result_page(query, page, size)
    return page
