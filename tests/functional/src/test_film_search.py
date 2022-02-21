# from http import HTTPStatus
# from typing import Callable
#
# import pytest
#
#
# @pytest.mark.usefixtures("data_setup")
# @pytest.mark.data_setup_params("movies", "movies_list.json")
# @pytest.mark.asyncio
# class TestMoviesList:
#     async def test_success(self, make_get_request: Callable):
#         response = await make_get_request("/film/search", {"query": "дружно"})
#
#         assert response.status == HTTPStatus.OK
#         assert len(response.body) == 2
#
#     async def test_check_query_and_paging(self, make_get_request: Callable):
#         # всего 3 совпадения со словом "угроза"
#         response = await make_get_request(
#             "/film/search", {"query": "угроза", "page[number]": 2, "page[size]": 2}
#         )
#
#         assert response.status == HTTPStatus.OK
#         assert len(response.body) == 1
