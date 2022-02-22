# from http import HTTPStatus
# from typing import Callable
#
# import pytest
#
#
# @pytest.mark.usefixtures("data_setup")
# @pytest.mark.data_setup_params("persons", "persons_list.json")
# @pytest.mark.asyncio
# class TestPersonsList:
#     async def test_success(self, make_get_request: Callable):
#         response = await make_get_request("/person/search", {"query": "Юрьевна"})
#
#         assert response.status == HTTPStatus.OK
#         assert len(response.body) == 2
#
#     async def test_check_query_and_paging(self, make_get_request: Callable):
#         response = await make_get_request(
#             "/person/search", {"query": "София", "page[number]": 2, "page[size]": 3}
#         )
#
#         assert response.status == HTTPStatus.OK
#         assert len(response.body) == 1
