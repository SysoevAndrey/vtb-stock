import inject

from catalog.application.request_mapper.filters_request import FiltersRequest
from catalog.core.domain.card import Card
from catalog.infrastructure.gateways.es_cards_query_service import ESCardsQueryService


class CardListService:
    @inject.autoparams()
    def __init__(self, es_cards_query_service: ESCardsQueryService):
        self._es_cards_query_service = es_cards_query_service

    async def match_cards(self, filters_request: FiltersRequest) -> list[Card]:
        cards = await self._es_cards_query_service.search_cards(filters_request)

        return cards
