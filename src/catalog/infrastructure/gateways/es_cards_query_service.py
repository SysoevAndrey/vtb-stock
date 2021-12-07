from typing import Any
from uuid import UUID

import inject
from elasticsearch import AsyncElasticsearch

from catalog.application.request_mapper.filters_request import FiltersRequest, SelectedParameter
from catalog.core.domain.card import Card


class ESCardsQueryService:
    @inject.autoparams()
    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        self._es_client = es_client
        self._index_name = index_name

    async def search_cards(self, filters_request: FiltersRequest) -> list[Card]:
        query = self._make_base_query(filters_request)
        sort_query = self._make_sort_query(filters_request.sort)
        from_ = (filters_request.page - 1) * filters_request.size
        search_result = await self._search_by_query(query, sort_query, from_=from_, size=filters_request.size)

        return self._extract_cards(search_result)

    @staticmethod
    def _extract_cards(es_response: dict[str, Any]) -> list[Card]:
        return [
            Card(
                id=UUID(hit["_id"]),
                image=hit["_source"]["search_result"]["image"],
                price=int(hit["_source"]["search_result"]["price"]),
                label=hit["_source"]["search_result"]["label"],
                rating=float(hit["_source"]["search_result"]["rating"]),
                reviews_count=int(hit["_source"]["search_result"]["reviews_count"]),
                path=hit["_source"]["search_result"]["path"],
            )
            for hit in es_response["hits"]["hits"]
        ]

    async def _search_by_query(
        self, query: dict[str, Any], sort: list[dict[str, Any]], from_: int, size: int
    ) -> dict[str, Any]:
        return await self._es_client.search(
            index=self._index_name,
            body={"query": query, "sort": sort, "from_": from_, "size": size, "track_total_hits": True},
        )

    def _make_base_query(self, filters_request: FiltersRequest) -> dict[str, Any]:
        return {
            "bool": {
                "filter": [
                    *self._make_search_query(filters_request.parameters),
                    self._make_categories_query(filters_request.categories),
                ],
            }
        }

    @staticmethod
    def _make_sort_query(sort_keys: list[str]) -> list[dict[str, Any]]:
        return [{key: {"order": "asc"}} for key in sort_keys]

    @staticmethod
    def _make_search_query(parameters: list[SelectedParameter]) -> list[dict[str, Any]]:
        return [
            {"terms": {f"search_data.{parameter.id}": parameter.selected_values}}
            if not parameter.selected_interval
            else {
                "range": {
                    f"search_data.{parameter.id}": {
                        "gte": parameter.selected_interval.gte,
                        "lte": parameter.selected_interval.lte,
                    }
                }
            }
            for parameter in parameters
        ]

    @staticmethod
    def _make_categories_query(categories: list[str]) -> dict[str, Any]:
        return {"term": {"categories.paths.tree": "root/" + "/".join(categories) if categories else "root"}}
