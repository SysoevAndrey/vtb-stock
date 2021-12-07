from functools import partial
from time import sleep

import inject
from elasticsearch import AsyncElasticsearch

from catalog.core.services.card_list_service import CardListService
from catalog.entrypoint.config import Config
from catalog.infrastructure.gateways.es_cards_query_service import ESCardsQueryService


def _configure(inject_binder: inject.Binder, config: Config):
    inject_binder.bind(Config, config)
    inject_binder.bind_to_constructor(
        AsyncElasticsearch,
        lambda: AsyncElasticsearch(hosts=[{"host": config.elasticsearch_host, "port": config.elasticsearch_port}]),
    )
    inject_binder.bind_to_constructor(ESCardsQueryService, ESCardsQueryService)  # type: ignore
    inject_binder.bind_to_constructor(CardListService, CardListService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
