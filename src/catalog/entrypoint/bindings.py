from functools import partial
from time import sleep

import inject
from elasticsearch import AsyncElasticsearch

from catalog.core.services.card_list_service import CardListService
from catalog.entrypoint.config import Config
from catalog.infrastructure.gateways.es_cards_query_service import ESCardsQueryService
from catalog.infrastructure.gateways.es_cards_save_service import ESCardsSaveService


def _configure(inject_binder: inject.Binder, config: Config):
    inject_binder.bind(Config, config)
    es_client = AsyncElasticsearch(hosts=[{"host": config.elasticsearch_host, "port": config.elasticsearch_port}])
    inject_binder.bind_to_constructor(
        AsyncElasticsearch,
        lambda: es_client,
    )
    inject_binder.bind_to_constructor(ESCardsQueryService, lambda: ESCardsQueryService(es_client=es_client, index_name=config.elasticsearch_cards_index))  # type: ignore
    inject_binder.bind_to_constructor(ESCardsSaveService, lambda: ESCardsSaveService(es_client=es_client, index_name=config.elasticsearch_cards_index))  # type: ignore
    inject_binder.bind_to_constructor(CardListService, CardListService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
