from typing import Optional
from fastapi.params import Query
import inject
from catalog.application.controllers.api_router import get_api_router
from fastapi_utils.cbv import cbv
from catalog.application.presentation.card_list_response import CardsPaginatedResponse, CardResponse
from catalog.application.presentation.hateoas import HateoasLinks, Link
from catalog.application.request_mapper.filters_request import FiltersRequestSchema
from catalog.core.services.card_list_service import CardListService
from loguru import logger

router = get_api_router()

mock_data = CardsPaginatedResponse.construct(
    items=[
        CardResponse.construct(
            id="382357c8-8547-41d1-9171-d23078dbfb60",
            label="Iphone 13",
            image="https://img.com/random",
            price=140000,
            rating=4.5,
            reviews_count=49,
            path="/stock/electronics/382357c8-8547-41d1-9171-d23078dbfb60",
        )
    ],
    links=HateoasLinks.construct(
        prev=None,
        self_=Link.construct(
            href="https://vtb-stock.com/catalog/api/cards?sort=cheaper&categories=electronics,smartphones&filters=minPrice=1000,maxPrice=10000&page=1&size=10",
            path="/catalog/api/cards?sort=cheaper&categories=electronics,smartphones&filters=minPrice=1000,maxPrice=10000&page=1&size=10",
        ),
        next_=None,
    ),
)


@cbv(router)
class CardListResource:
    filters_request_schema = FiltersRequestSchema()

    @router.get(
        "/api/products/cards",
        response_model=CardsPaginatedResponse,
        response_model_exclude_none=True,
        response_model_by_alias=True,
        response_description="Successful response",
    )
    async def get_cards_by_filters(
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
        service = inject.instance(CardListService)
        filters_request = self.filters_request_schema.load(
            {"categories": categories, "sort": sort, "search": search, "filters": filters}
        )
        logger.info(filters_request)
        return mock_data
