from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from core.config import Settings
from services.genre import GenreService, get_genre_service

router = APIRouter()

settings = Settings()


class Genre(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    films: Optional[List[dict]]


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.GENRES_NOT_FOUND
        )
    return Genre(
        id=genre.id, name=genre.name, description=genre.description, films=genre.films
    )


@router.get("/search/")
async def search_genre(
    genre: Optional[str] = Query(None, max_length=50),
    page_size: Optional[int] = Query(default=10),
    page_number: Optional[int] = Query(default=1),
    genre_service: GenreService = Depends(get_genre_service),
) -> dict:
    genres = await genre_service.search_genres(page_size, page_number, genre)
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=settings.GENRES_NOT_FOUND
        )
    return genres
