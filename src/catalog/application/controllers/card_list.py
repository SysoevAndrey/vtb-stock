from typing import Optional

import inject
from fastapi.params import Query
from fastapi_utils.cbv import cbv
from loguru import logger

from catalog.application.controllers.api_router import get_api_router
from catalog.application.presentation.card_list_response import (
    CardResponse,
    CardsPaginatedResponse,
    CardsPaginatedResponsePresentationSchema,
)
from catalog.application.presentation.hateoas import HateoasLinks, Link
from catalog.application.presentation.save_cards_response import (
    SaveCardsResponseModel,
    SaveCardsResponseModelPresentationSchema,
)
from catalog.application.request_mapper.card_document_create_request import CardDocumentCreateRequest
from catalog.application.request_mapper.filters_request import FiltersRequestSchema
from catalog.core.services.card_list_service import CardListService

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
    card_documents_response_schema = SaveCardsResponseModelPresentationSchema()
    cards_paginated_response_schema = CardsPaginatedResponsePresentationSchema()

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
        cards, total_elements = await service.match_cards(filters_request)
        return self.cards_paginated_response_schema.dump({"total_elements": total_elements, "items": cards})

    @router.post(
        "/api/products/cards",
        responses={"200": {"description": "One or more cards successfully created", "model": SaveCardsResponseModel}},
    )
    async def save_card_documents(
        self, card_documents_create_request: list[CardDocumentCreateRequest]
    ) -> SaveCardsResponseModel:
        service = inject.instance(CardListService)
        success, failed = await service.save_card_documents(card_documents_create_request)

        return self.card_documents_response_schema.dump({"success_count": success, "failed_count": failed})
