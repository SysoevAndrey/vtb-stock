import asyncio

from elasticsearch._async.client import AsyncElasticsearch
from catalog.entrypoint.config import Config
from catalog.infrastructure.gateways.es_cards_save_service import ESCardsSaveService


async def main(config_obj: Config):
    es_client = AsyncElasticsearch(
        hosts=[{"host": config_obj.elasticsearch_host, "port": config_obj.elasticsearch_port}]
    )
    service = ESCardsSaveService(es_client=es_client, index_name=config_obj.elasticsearch_cards_index)

    await service.create_index_if_not_exists()


if __name__ == "__main__":
    asyncio.run(main(Config()))
