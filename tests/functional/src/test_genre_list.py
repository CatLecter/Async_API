from http import HTTPStatus
from uuid import uuid4
import pytest


@pytest.mark.asyncio
async def test_genres_list(create_index, make_get_request):
    response = await make_get_request(method="/genres/", params={})
    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == 7


@pytest.mark.asyncio
async def test_genres_search(create_index, make_get_request):
    response = await make_get_request("/genres/", params={"query": "Fantasy"})
    assert response.status == HTTPStatus.OK
    assert response.body["items"][0]["name"] == "Fantasy"
