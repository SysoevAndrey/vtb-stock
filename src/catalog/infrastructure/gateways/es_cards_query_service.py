import json
from typing import Any
from uuid import UUID

import inject
from elasticsearch import AsyncElasticsearch

from catalog.application.request_mapper.filters_request import FiltersRequest, SelectedParameter
from catalog.core.domain.available_parameter import AvailableValue, ParameterStats
from catalog.core.domain.card import Card
from catalog.infrastructure.gateways.models.aggs_result import CategoryAgg, FiltersAggregationResult, KeywordParameterAgg, NumberParameterAgg, SortKeyAgg


class ESCardsQueryService:
    faceted_aggregation_query = {
        "keyword_parameters_stats": {
            "nested": {"path": "keyword_parameters"},
            "aggs": {
                "name": {
                    "terms": {"field": "keyword_parameters.facet_info", "size": 100},
                    "aggs": {"parameter_values": {"terms": {"field": "keyword_parameters.facet_value", "size": 10000}}},
                }
            },
        },
        "number_parameters_stats": {
            "nested": {"path": "number_parameters"},
            "aggs": {
                "name": {
                    "terms": {"field": "number_parameters.facet_info", "size": 100},
                    "aggs": {"parameter_values": {"stats": {"field": "number_parameters.value"}}},
                }
            },
        },
        "categories_stats": {
            "nested": {"path": "categories"},
            "aggs": {"name": {"terms": {"field": "categories.facet_info"}}},
        },
        "sort_keys_stats": {
            "nested": {"path": "number_sort_parameters"},
            "aggs": {"name": {"terms": {"field": "number_sort_parameters.facet_info"}}},
        },
    }

    @inject.autoparams()
    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        self._es_client = es_client
        self._index_name = index_name

    async def faceted_aggs(self, filters_request: FiltersRequest) -> FiltersAggregationResult:
        query = self._make_base_query(filters_request)
        aggs_result = await self._search_by_query(query, aggs=self.faceted_aggregation_query)
        return self._build_filters_aggregations_result(aggs_result)

    def _build_filters_aggregations_result(self, aggs_result: dict[str, Any]) -> FiltersAggregationResult:
        keyword_parameters_aggs = self._build_keyword_parameters_aggs(
            aggs_result["aggregations"]["keyword_parameters_stats"]["name"]["buckets"]
        )
        number_parameters_aggs = self._build_number_parameters_aggs(
            aggs_result["aggregations"]["number_parameters_stats"]["name"]["buckets"]
        )
        sort_keys_aggs = self._build_sort_keys_aggs(aggs_result["aggregations"]["sort_keys_stats"]["name"]["buckets"])
        categories_stats_aggs = self._build_categories_stats_aggs(
            aggs_result["aggregations"]["categories_stats"]["name"]["buckets"]
        )

        return FiltersAggregationResult(
            number_parameters_aggs=number_parameters_aggs,
            keyword_parameters_aggs=keyword_parameters_aggs,
            sort_key_aggs=sort_keys_aggs,
            category_aggs=categories_stats_aggs,
        )

    def _build_keyword_parameters_aggs(self, buckets: list[dict[str, Any]]) -> list[KeywordParameterAgg]:
        params = []
        for bucket in buckets:
            param_info = json.loads(bucket["key"])
            doc_count = bucket["doc_count"]

            values = []
            for value_bucket in bucket["parameter_values"]["buckets"]:
                value_info = json.loads(value_bucket["key"])
                values.append(
                    AvailableValue(
                        id=value_info["id"],
                        label=value_info["label"],
                        doc_count=value_bucket["doc_count"]
                    )
                )
            params.append(
                KeywordParameterAgg(
                    doc_count=doc_count,
                    label=param_info["label"],
                    id=param_info["id"],
                    available_values=values.copy()
                )
            )
        return params

    def _build_sort_keys_aggs(self, buckets: list[dict[str, Any]]) -> list[SortKeyAgg]:
        params = []
        for bucket in buckets:
            param_info = json.loads(bucket["key"])
            doc_count = bucket["doc_count"]

            params.append(
                SortKeyAgg(
                    doc_count=doc_count,
                    label=param_info["label"],
                    id=param_info["id"],
                )
            )
        return params

    def _build_categories_stats_aggs(self, buckets: list[dict[str, Any]]) -> list[CategoryAgg]:
        params = []
        for bucket in buckets:
            param_info = json.loads(bucket["key"])
            doc_count = bucket["doc_count"]

            params.append(
                CategoryAgg(
                    doc_count=doc_count,
                    label=param_info["label"],
                    id=param_info["id"],
                    image=param_info["image"],
                    parent=param_info["parent"],
                )
            )
        return params

    def _build_number_parameters_aggs(self, buckets: list[dict[str, Any]]) -> list[NumberParameterAgg]:
        params = []
        for bucket in buckets:
            param_info = json.loads(bucket["key"])
            doc_count = bucket["doc_count"]

            param_stats = bucket["parameter_values"]
            params.append(
                NumberParameterAgg(
                    doc_count=doc_count,
                    label=param_info["label"],
                    id=param_info["id"],
                    value_stats=ParameterStats(
                        minimum=param_stats["min"],
                        maximum=param_stats["max"],
                        average=param_stats["avg"],
                        total_sum=param_stats["sum"],
                    )
                )
            )
        return params

    async def search_cards(self, filters_request: FiltersRequest) -> tuple[list[Card], int]:
        query = self._make_base_query(filters_request)
        sort_query = self._make_sort_query(filters_request.sort)
        from_ = (filters_request.page - 1) * filters_request.size
        search_result = await self._search_by_query(query, sort_query, from_=from_, size=filters_request.size)

        return self._extract_cards(search_result), search_result["hits"]["total"]["value"]

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
        self,
        query: dict[str, Any],
        sort: list[dict[str, Any]] = None,
        from_: int = 0,
        size: int = 0,
        aggs: dict[str, Any] = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query, "from": from_, "size": size, "track_total_hits": True}
        if sort:
            body["sort"] = sort
        if aggs:
            body["aggs"] = aggs
        return await self._es_client.search(
            index=self._index_name,
            body=body,
        )

    def _make_base_query(self, filters_request: FiltersRequest) -> dict[str, Any]:
        search_query = self._make_search_query(filters_request.parameters)
        categories_query = self._make_categories_query(filters_request.categories)
        return (
            {
                "bool": {
                    "filter": [
                        *search_query,
                        *categories_query,
                    ],
                }
            }
            if search_query or categories_query
            else {"match_all": {}}
        )

    @staticmethod
    def _make_sort_query(sort_keys: list[str]) -> list[dict[str, Any]]:
        return [{f"sort_numbers_data.{key}": {"order": "asc"}} for key in sort_keys]

    @staticmethod
    def _make_search_query(parameters: list[SelectedParameter]) -> list[dict[str, Any]]:
        return [
            {"terms": {f"keyword_search_data.{parameter.id}": parameter.selected_values}}
            if not parameter.selected_interval
            else {
                "range": {
                    f"number_search_data.{parameter.id}": {
                        "gte": parameter.selected_interval.gte,
                        "lte": parameter.selected_interval.lte,
                    }
                }
            }
            for parameter in parameters
        ]

    @staticmethod
    def _make_categories_query(categories: list[str]) -> list[dict[str, Any]]:
        return [{"term": {"categories_navigation.path": category}} for category in categories]
