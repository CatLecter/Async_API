import pytest


@pytest.mark.asyncio
async def test_search_person(
    create_index,
    make_get_request,
    expected_json_response,
):
    response = await make_get_request("/persons/search/", params={"query": "David"})
    assert response.status == 200
    assert response.body == expected_json_response


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


#
#
# @pytest.mark.asyncio
# async def test_person_by_id(make_get_request,
#                             initialize_environment,
#                             expected_json_response):
#     some_id = "239f6e94-b317-4f10-bb0c-ef86dfe33d8a"
#     response = await make_get_request(f"/person/{some_id}")
#     assert response.status == 200
#     assert response.body == expected_json_response
#
#
# @pytest.mark.asyncio
# async def test_person_films_by_id(make_get_request,
#                                   initialize_environment,
#                                   expected_json_response):
#     some_id = "239f6e94-b317-4f10-bb0c-ef86dfe33d8a"
#     response = await make_get_request(f"/person/{some_id}/film")
#     assert response.status == 200
#     assert response.body == expected_json_response
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     (
#             'page_number', 'page_size'
#     ),
#     (
#             (1, 1),
#             ("1", "1"),
#             (1, 5),
#             (5, 1),
#             (1, 4164),  # total number of persons
#     )
# )
# async def test_search_person_pagination(make_get_request,
#                                         initialize_environment,
#                                         page_number,
#                                         page_size):
#     """Pagination tests for common cases"""
#     # only check response status and number of elements here
#     response = await make_get_request("/person/search/",
#                                       params={
#                                           "page[number]": page_number,
#                                           "page[size]": page_size}
#                                       )
#     assert response.status == 200
#     assert len(response.body) == int(page_size)
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     (
#             'page_number', 'page_size', 'expected_count'
#     ),
#     (
#             (1, 10000, 4164),  # we don't have that many persons in index
#             (42, 100, 64),
#             (100, 100, 0),
#     )
# )
# async def test_search_person_pagination_borders(make_get_request,
#                                                 initialize_environment,
#                                                 page_number,
#                                                 page_size,
#                                                 expected_count):
#     response = await make_get_request("/person/search/",
#                                       params={
#                                           "page[number]": page_number,
#                                           "page[size]": page_size}
#                                       )
#     assert response.status == 200
#     assert len(response.body) == expected_count
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     (
#             'page_number', 'page_size'
#     ),
#     (
#             (-1, 5),
#             (-1, -1),
#             (1, -1),
#             ("str_number", "str_size"),
#             (1.5, 1.7),
#     )
# )
# async def test_search_person_pagination_invalid_input(make_get_request,
#                                                       initialize_environment,
#                                                       page_number,
#                                                       page_size):
#     response = await make_get_request("/person/search/",
#                                       params={
#                                           "page[number]": page_number,
#                                           "page[size]": page_size}
#                                       )
#     assert response.status == 422
