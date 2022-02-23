import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_films_search(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request("/films/search/", params={"query": "Star"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_films_search_not_found(
    create_index, make_get_request, expected_json_response
):
    response = await make_get_request("/films/search/", params={"query": "NotFound"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_films_pagination(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request(
        "/films/search/",
        params={
            "page[number]": 2,
            "page[size]": 4
        }
    )
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_films_all(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request(
        "/films/search/",
        params={
            "page[number]": 1,
            "page[size]": 10
        }
    )
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response
