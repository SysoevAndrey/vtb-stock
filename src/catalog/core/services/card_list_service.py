from typing import Optional

import inject

from catalog.application.request_mapper.card_document_create_request import (
    CardCategoryCreateRequest,
    CardDocumentCreateRequest,
)
from catalog.application.request_mapper.filters_request import FiltersRequest
from catalog.core.domain.card import Card
from catalog.core.domain.card_document import CardCategory, CardDocument, KeywordParameter, NumberParameter
from catalog.infrastructure.gateways.es_cards_query_service import ESCardsQueryService
from catalog.infrastructure.gateways.es_cards_save_service import ESCardsSaveService


class CardListService:
    @inject.autoparams()
    def __init__(self, es_cards_query_service: ESCardsQueryService, es_cards_save_service: ESCardsSaveService):
        self._es_cards_query_service = es_cards_query_service
        self._es_cards_save_service = es_cards_save_service

    async def match_cards(self, filters_request: FiltersRequest) -> tuple[list[Card], int]:
        cards, total = await self._es_cards_query_service.search_cards(filters_request)

        return cards, total

    async def save_card_documents(
        self, card_documents_create_request: list[CardDocumentCreateRequest]
    ) -> tuple[int, int]:
        card_documents = self._build_card_documents(card_documents_create_request)

        success_count, failed_count = await self._es_cards_save_service.bulk_save_documents(card_documents)
        return success_count, failed_count

    @staticmethod
    def _build_card_documents(card_documents_create_request: list[CardDocumentCreateRequest]) -> list[CardDocument]:
        card_documents: list[CardDocument] = []

        for card_document_request in card_documents_create_request:
            categories = []
            prev_category: Optional[CardCategoryCreateRequest] = None
            for category in card_document_request.categories:
                categories.append(
                    CardCategory(
                        id=category.id,
                        parent=prev_category.id if prev_category else None,
                        image=category.image,
                        label=category.label,
                    )
                )
                prev_category = category.copy()

            card_documents.append(
                CardDocument(
                    item=Card(
                        id=card_document_request.item.id,
                        image=card_document_request.item.image,
                        label=card_document_request.item.label,
                        price=card_document_request.item.price,
                        rating=card_document_request.item.rating,
                        reviews_count=card_document_request.item.reviews_count,
                        path=card_document_request.item.path,
                    ),
                    number_parameters=[
                        NumberParameter(id=parameter.id, label=parameter.label, value=parameter.value)
                        for parameter in card_document_request.number_parameters
                    ],
                    keyword_parameters=[
                        KeywordParameter(
                            id=parameter.id,
                            label=parameter.label,
                            values=parameter.values,
                        )
                        for parameter in card_document_request.keyword_parameters
                    ],
                    categories=categories.copy(),
                    type="products",
                )
            )
        return card_documents
