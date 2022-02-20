import pytest

# https://www.youtube.com/watch?v=MIHXRF6YMN4
# todo: УДАЛИТЬ ЭТОТ ФАЙЛ ПЕРЕД СДАЧЕЙ!

def test_simple():
    assert 10 / 2 == 5


@pytest.mark.parametrize("a, b, c", [(10, 5, 2),
                                     (10, 2, 5)])
def test_simple_2(a, b, c):
    assert int(a) / int(b) == int(c)


def test_error():
    with pytest.raises(TypeError):
        a = 10 / "2"



# @pytest.mark.asyncio
# async def test_search_detailed(es_client):
#     # Заполнение данных для теста
#     await es_client.bulk(...)
#
#     # Выполнение запроса
#     response = await make_get_request('/search', {'search': 'Star Wars'})
#
#     # Проверка результата
#     assert response.status == 200
#     assert len(response.body) == 1
#
#     assert response.body == expected
