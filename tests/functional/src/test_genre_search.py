from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_genres_all_list(create_index, make_get_request, test_data):
    response = await make_get_request(method="/genres/", params={})
    genres_test_data = await test_data("genres")
    expected_items = [{"uuid": item["uuid"], "name": item["name"]} for item in genres_test_data]
    assert response.status == HTTPStatus.OK
    assert response.body["items"] == expected_items
    assert response.body["total"] == len(expected_items)
    assert response.body["page_size"] is None
    assert response.body["page_number"] is None


@pytest.mark.asyncio
async def test_genres_search(create_index, make_get_request, test_data):
    response = await make_get_request("/genres/", params={"query": "Fantasy"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response

    expected_result = await test_data("genres")
    for i in range(len(expected_result)):
        tested_genre = expected_result[i]
        response = await make_get_request(f"/genres/{tested_genre['uuid']}", params={})
        assert response.status == HTTPStatus.OK
        assert response.body == tested_genre


@pytest.mark.asyncio
async def test_genres_search_not_found(
    create_index, make_get_request, expected_json_response
):
    response = await make_get_request("/genres/", params={"query": "NotFound"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response
