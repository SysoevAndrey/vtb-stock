from typing import Optional
from fastapi.params import Query
import inject
from catalog.application.controllers.api_router import get_api_router
from fastapi_utils.cbv import cbv
from catalog.application.presentation.filters_list_response import (
    AvailableValueResponse,
    CategoryResponse,
    FiltersListResponse,
    ParameterResponse,
    ParameterStatsResponse,
    SortKeyResponse,
    SubCategoryResponse,
)
from catalog.application.request_mapper.filters_request import FiltersRequestSchema
from loguru import logger

from catalog.core.domain.available_parameter import ParameterType

router = get_api_router()

mock_data = FiltersListResponse.construct(
    parameters=[
        ParameterResponse.construct(
            id="brand",
            label="Производитель",
            type=ParameterType.KEYWORD,
            available_values=[
                AvailableValueResponse.construct(id="apple", label="Apple", doc_count=32),
                AvailableValueResponse.construct(id="samsung", label="Samsung", doc_count=105),
                AvailableValueResponse.construct(id="huawei", label="Huawei", doc_count=345),
                AvailableValueResponse.construct(id="xiaomi", label="Xiaomi", doc_count=1032),
            ],
        ),
        ParameterResponse.construct(
            id="color",
            label="Цвет",
            type=ParameterType.KEYWORD,
            available_values=[
                AvailableValueResponse.construct(id="red", label="Красный", doc_count=32),
                AvailableValueResponse.construct(id="blue", label="Синий", doc_count=105),
                AvailableValueResponse.construct(id="black", label="Черный", doc_count=345),
                AvailableValueResponse.construct(id="white", label="Белый", doc_count=1032),
            ],
        ),
        ParameterResponse.construct(
            id="color",
            label="Цвет",
            type=ParameterType.KEYWORD,
            available_values=[
                AvailableValueResponse.construct(id="red", label="Красный", doc_count=32),
                AvailableValueResponse.construct(id="blue", label="Синий", doc_count=105),
                AvailableValueResponse.construct(id="black", label="Черный", doc_count=345),
                AvailableValueResponse.construct(id="white", label="Белый", doc_count=1032),
            ],
        ),
        ParameterResponse.construct(
            id="shop",
            label="Продавец",
            type=ParameterType.KEYWORD,
            available_values=[
                AvailableValueResponse.construct(id="mvideo", label="М-Видео", doc_count=32),
                AvailableValueResponse.construct(id="eldorado", label="Эльдорадо", doc_count=105),
                AvailableValueResponse.construct(id="dns", label="DNS", doc_count=345),
                AvailableValueResponse.construct(id="city_link", label="City-Link", doc_count=1032),
            ],
        ),
        ParameterResponse.construct(
            id="price",
            label="Цена",
            type=ParameterType.NUMBER,
            available_values=[],
            stats=ParameterStatsResponse.construct(
                minimum=1000,
                maximum=125000,
                average=40000,
                total_sum=1000000,
            ),
        ),
    ],
    categories=[
        CategoryResponse.construct(
            id="electronics",
            label="Электроника",
            image="",
            path="/api/products/filters?categories=electronics",
            sub_categories=[
                SubCategoryResponse.construct(
                    id="smartphones",
                    label="Смартфоны",
                    path="/api/products/filters?categories=electronics,smartphones",
                ),
                SubCategoryResponse.construct(
                    id="accessories",
                    label="Аксессуары",
                    path="/api/products/filters?categories=electronics,accessories",
                ),
                SubCategoryResponse.construct(
                    id="button_phones",
                    label="Кнопочные телефоны",
                    path="/api/products/filters?categories=electronics,button_phones",
                ),
            ],
        )
    ],
    sort=[
        SortKeyResponse.construct(id="cheaper", label="Сначала дешевле"),
        SortKeyResponse.construct(id="rating", label="Сначала с высокими оценками")
    ],
)


@cbv(router)
class FiltersListResource:
    filters_request_schema = FiltersRequestSchema()

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
        filters_request = self.filters_request_schema.load(
            {"categories": categories, "sort": sort, "search": search, "filters": filters}
        )
        logger.info(filters_request)
        return mock_data
