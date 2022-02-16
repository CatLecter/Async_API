from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Term, Nested

from search.general import SearchEngine, SearchParams, SearchResult


class ElasticSearchEngine(SearchEngine):
    """Класс поискового движка ElasticSearch."""

    def __init__(self, service: AsyncElasticsearch):
        self.elastic = service

    async def get_by_pk(self, table: str, pk: str) -> SearchResult:
        """Возвращает объект по ключу."""
        result = SearchResult(items=[], total=0)
        try:
            doc = await self.elastic.get(index=table, id=pk)
        except NotFoundError:
            return result
        result.items = [doc['_source']]
        result.total = 1
        return result

    async def search(self, table: str, params: SearchParams) -> SearchResult:
        """Возвращает объекты подходящие под параметры поиска."""
        try:
            search = Search(using=self.elastic)
            if params.query_fields:
                search = search.query(
                    MultiMatch(
                        query=params.query_value,
                        fields=params.query_fields,
                        operator='and',
                        fuzziness='AUTO',
                    )
                )
            if params.sort_field:
                search = search.sort(params.sort_field)
            if params.filter_field:
                search = search.query(
                    Nested(path=params.filter_field, query=Term(**{f'{params.filter_field}__uuid': params.filter_value}))
                )
            start = (params.page_number - 1) * params.page_size
            end = start + params.page_size
            search = search[start:end]
            body = search.to_dict()
            docs = await self.elastic.search(index=table, body=body)
        except NotFoundError:
            return SearchResult(items=[], total=0)
        result = SearchResult(
            items=[doc['_source'] for doc in docs['hits']['hits']],
            total=docs['hits']['total']['value'],
        )
        return result
