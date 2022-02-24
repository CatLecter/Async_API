import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_persons_search(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request("/persons/search/", params={"query": "David"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_persons_search_not_found(
    create_index, make_get_request, expected_json_response
):
    response = await make_get_request("/persons/search/", params={"query": "NotFound"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_persons_pagination(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request(
        "/persons/search/",
        params={
            "page[number]": 3,
            "page[size]": 20
        }
    )
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_persons_all(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request(
        "/persons/search/",
        params={
            "page[number]": 1,
            "page[size]": 65
        }
    )
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response
