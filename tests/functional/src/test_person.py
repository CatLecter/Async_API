from http import HTTPStatus
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_person(create_index, make_get_request, expected_json_response):
    _uuid = "3499da28-d6ba-4d4a-8f7e-81c09c6b0912"
    response = await make_get_request(f"/persons/{_uuid}", params={})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_person_not_found(create_index, make_get_request):
    _uuid = uuid4()
    response = await make_get_request(f"/persons/{_uuid}", params={})
    assert response.status == HTTPStatus.NOT_FOUND
