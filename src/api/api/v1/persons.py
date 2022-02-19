from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from core.config import NOT_FOUND_MESSAGE
from core.endpoints_params import *
from models.general import Page
from models.person import Person, PersonBrief
from services.getters import get_person_service
from services.person import PersonService

router = APIRouter(prefix='/persons', tags=['Персоны'])


@router.get(
    path='/{uuid}',
    name='Детали персоны',
    description='Получение детальной информации по персоне.',
    response_model=Person,
)
async def person_details(
    uuid: str = Query(**DEFAULT_UUID),
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_uuid(uuid)
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
    query: str = Query(**DEFAULT_QUERY),
    page_number: Optional[int] = Query(**DEFAULT_PAGE_NUMBER),
    page_size: Optional[int] = Query(**DEFAULT_PAGE_SIZE),
    person_service: PersonService = Depends(get_person_service),
) -> Page[PersonBrief]:
    page = await person_service.search(query, page_number, page_size)
    return page
