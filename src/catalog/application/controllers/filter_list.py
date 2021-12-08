from typing import Optional

import inject
from fastapi.params import Query
from fastapi_utils.cbv import cbv
from loguru import logger

from catalog.application.controllers.api_router import get_api_router
from catalog.application.presentation.filters_list_response import (
    FiltersListResponse,
    FiltersListResponsePresentationSchema,
)
from catalog.application.request_mapper.filters_request import FiltersRequestSchema
from catalog.core.services.relevant_filters_service import RelevantFiltersService

router = get_api_router()


@cbv(router)
class FiltersListResource:
    filters_request_schema = FiltersRequestSchema()
    filters_response_schema = FiltersListResponsePresentationSchema()

    @router.get(
        "/api/products/filters",
        response_model=FiltersListResponse,
        response_model_exclude_none=True,
        response_model_by_alias=True,
        response_description="Successful response",
    )
    async def get_available_filters(
        self,
        categories: list[str] = Query(  # type: ignore
            [], description="Путь по иерархии категорий", example=["electronics", "smartphones"]  # type: ignore
        ),  # type: ignore
        sort: list[str] = Query(  # type: ignore
            [], description="Теги для сортировки", example=["cheaper"]  # type: ignore
        ),  # type: ignore
        search: Optional[str] = Query(  # type: ignore
            None, description="Строка для полнотекстового поиска", example="Iphone 13"  # type: ignore
        ),  # type: ignore
        filters: list[str] = Query(  # type: ignore
            [], description="Фильтры для фасетного поиска", example=["minPrice=1000", "maxPrice=10000", "brand=apple;samsung"]  # type: ignore
        ),  # type: ignore
    ):
        service = inject.instance(RelevantFiltersService)
        filters_request = self.filters_request_schema.load(
            {"categories": categories, "sort": sort, "search": search, "filters": filters}
        )
        logger.info(filters_request)
        filters_result = await service.calculate_relevant_filters(filters_request=filters_request)
        return self.filters_response_schema.dump(filters_result)
