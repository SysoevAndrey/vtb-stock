import inject

from catalog.application.request_mapper.card_document_create_request import (
    CardCategoryCreateRequest,
    CardDocumentCreateRequest,
)
from catalog.application.request_mapper.filters_request import FiltersRequest
from catalog.core.domain.available_parameter import AvailableParameter, ParameterType
from catalog.core.domain.card import Card
from catalog.core.domain.card_document import CardCategory, CardDocument, KeywordParameter, NumberParameter
from catalog.core.domain.category import Category
from catalog.core.domain.filters_result import FiltersResult
from catalog.core.domain.sort_key import SortKey
from catalog.infrastructure.gateways.es_cards_query_service import ESCardsQueryService
from catalog.infrastructure.gateways.es_cards_save_service import ESCardsSaveService
from catalog.infrastructure.gateways.models.aggs_result import (
    CategoryAgg,
    FiltersAggregationResult,
    KeywordParameterAgg,
    NumberParameterAgg,
)


class RelevantFiltersService:
    @inject.autoparams()
    def __init__(self, es_cards_query_service: ESCardsQueryService, es_cards_save_service: ESCardsSaveService):
        self._es_cards_query_service = es_cards_query_service

    async def calculate_relevant_filters(self, filters_request: FiltersRequest) -> FiltersResult:
        raw_filters_result = await self._es_cards_query_service.faceted_aggs(filters_request)

        return self._build_filters_result(raw_filters_result)

    def _build_filters_result(self, filters_aggs_result: FiltersAggregationResult) -> FiltersResult:
        parameter_stats = self._merge_parameters(
            filters_aggs_result.keyword_parameters_aggs, filters_aggs_result.number_parameters_aggs
        )
        categories_tree = self._build_categories_tree(filters_aggs_result.category_aggs)

        return FiltersResult(
            parameters=parameter_stats,
            categories=categories_tree,
            sort=[
                SortKey(id=sort_key_agg.id, label=sort_key_agg.label)
                for sort_key_agg in filters_aggs_result.sort_key_aggs
            ],
        )

    def _build_categories_tree(self, category_stats: list[CategoryAgg]) -> list[Category]:
        return [
            Category(
                id=category_agg.id,
                label=category_agg.label,
                image=category_agg.image,
                sub_categories=self._build_category_dependencies(category_agg.id, category_stats),
            )
            for category_agg in category_stats
        ]

    def _build_category_dependencies(self, identifier: str, category_stats: list[CategoryAgg]) -> list[Category]:
        direct_dependencies = [category_agg for category_agg in category_stats if category_agg.parent == identifier]
        return [
            Category(
                id=category_agg.id,
                label=category_agg.label,
                image=category_agg.image,
                sub_categories=self._build_category_dependencies(category_agg.id, category_stats),
            )
            for category_agg in direct_dependencies
        ]

    @staticmethod
    def _merge_parameters(
        keyword_params_stats: list[KeywordParameterAgg], number_params_stats: list[NumberParameterAgg]
    ) -> list[AvailableParameter]:
        params = []

        for keyword_param_agg in keyword_params_stats:
            params.append(
                AvailableParameter(
                    id=keyword_param_agg.id,
                    label=keyword_param_agg.label,
                    type=ParameterType.KEYWORD,
                    stats=None,
                    available_values=keyword_param_agg.available_values.copy(),
                )
            )

        for number_param_agg in number_params_stats:
            params.append(
                AvailableParameter(
                    id=number_param_agg.id,
                    label=number_param_agg.label,
                    type=ParameterType.NUMBER,
                    stats=number_param_agg.value_stats,
                    available_values=[],
                )
            )

        return params
