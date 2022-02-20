from uuid import uuid4
from http import HTTPStatus
from typing import Callable

import pytest


@pytest.mark.usefixtures("data_setup")
@pytest.mark.data_setup_params("genres", "genres_list.json")
@pytest.mark.asyncio
class TestGenreDetail:
    async def test_success(self, make_get_request: Callable):
        response = await make_get_request(
            "/genre/{uuid}".format(uuid="03c54c71-fca0-4536-a169-df82b9bdee2d"), {}
        )

        assert response.status == HTTPStatus.OK
        assert response.body["uuid"] == "03c54c71-fca0-4536-a169-df82b9bdee2d"
        assert response.body.get("name", None)

    async def test_not_found(self, make_get_request: Callable):
        response = await make_get_request("/genre/{uuid}".format(uuid=uuid4()))

        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body == {"detail": "genre not found"}
