from http import HTTPStatus
from typing import Callable

import pytest


@pytest.mark.usefixtures("data_setup")
@pytest.mark.data_setup_params("genres", "genres_list.json")
@pytest.mark.asyncio
class TestGenreList:
    async def test_success(self, make_get_request: Callable):
        response = await make_get_request("/genre", {})

        assert response.status == HTTPStatus.OK
        assert len(response.body) == 15
        assert response.body[0].get("name", None)

    async def test_check_paging_out_of_range(self, make_get_request: Callable):
        response = await make_get_request(
            "/genre", {"page[number]": 2, "page[size]": 15}
        )

        assert response.status == HTTPStatus.OK
        assert len(response.body) == 0

    async def test_check_paging_page_size(self, make_get_request: Callable):
        response = await make_get_request(
            "/genre", {"page[number]": 4, "page[size]": 3}
        )

        assert response.status == HTTPStatus.OK
        assert len(response.body) == 3
