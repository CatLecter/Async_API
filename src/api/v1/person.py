from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from core.config import Settings
from services.person import PersonService, get_person_service

router = APIRouter()

settings = Settings()


class Id(BaseModel):
    id: str


class Person(Id):
    full_name: Optional[str]
    role: Optional[str]
    film_ids: Optional[List[Id]]


@router.get("/{person_id}", response_model=Person)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.PERSONS_NOT_FOUND
        )
    return Person(
        id=person.id,
        full_name=person.full_name,
        role=person.role,
        film_ids=person.film_ids,
    )


@router.get("/{person_id}/film")
async def films_by_person(
    person_id: str, person_service: PersonService = Depends(get_person_service)
):
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.PERSONS_NOT_FOUND
        )
    return person.film_ids


@router.get("/search/")
async def search_person(
    person: Optional[str] = Query(None, max_length=50),
    page_size: Optional[int] = Query(default=1000),
    page_number: Optional[int] = Query(default=1),
    filter_field: Optional[str] = Query(default="role"),
    filter_value: Optional[str] = Query(default="actor"),
    sort_field: Optional[str] = Query(default="role"),
    person_service: PersonService = Depends(get_person_service),
) -> dict:
    persons = await person_service.search_persons(
        page_size, page_number, person, sort_field, filter_field, filter_value
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.PERSONS_NOT_FOUND
        )
    return persons
