from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_genres_list(create_index, make_get_request, expected_json_response):
    response = await make_get_request(method="/genres/", params={})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_genres_search(create_index, make_get_request, expected_json_response):
    response = await make_get_request("/genres/", params={"query": "Fantasy"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_genres_search_not_found(
    create_index, make_get_request, expected_json_response
):
    response = await make_get_request("/genres/", params={"query": "NotFound"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response
