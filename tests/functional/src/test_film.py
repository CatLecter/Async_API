from http import HTTPStatus
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_film(create_index, make_get_request, expected_json_response):
    _uuid = "6ca6dcd7-cd61-4db1-b9c3-efa531d5ea9a"
    response = await make_get_request(f"/films/{_uuid}", params={})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_film_not_found(create_index, make_get_request):
    _uuid = uuid4()
    response = await make_get_request(f"/films/{_uuid}", params={})
    assert response.status == HTTPStatus.NOT_FOUND
