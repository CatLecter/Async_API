from http import HTTPStatus
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_genre(create_index, make_get_request, expected_json_response):
    _uuid = "87751d4c-a850-4e2c-84dc-da6a797d76de"
    response = await make_get_request(f"/genres/{_uuid}", params={})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_genre_not_found(create_index, make_get_request):
    _uuid = uuid4()
    response = await make_get_request(f"/genres/{_uuid}", params={})
    assert response.status == HTTPStatus.NOT_FOUND
