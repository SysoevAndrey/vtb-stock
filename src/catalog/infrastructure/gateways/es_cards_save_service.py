import json
from pathlib import Path
from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from catalog.core.domain.card_document import CardDocument

from catalog.infrastructure.gateways.persistence.card_document_schema import CardDocumentPersistenceSchema

CUR_DIR = Path(__file__).resolve().parent


class ESCardsSaveService:
    document_schema = CardDocumentPersistenceSchema()

    mapping_path = CUR_DIR / "mappings" / "cards_mapping.json"

    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        self._es_client = es_client
        self._index_name = index_name

        self._mapping = self._initialize_mapping()

    def _initialize_mapping(self) -> dict[str, Any]:
        with open(self.mapping_path) as f:
            return json.load(f)

    async def put_mapping(self):
        await self._es_client.indices.put_mapping(body=self._mapping, index=self._index_name)

    async def bulk_save_documents(self, card_documents: list[CardDocument]):
        await async_bulk(self._es_client, actions=(self._document_serialize(document) for document in card_documents))

    def _document_serialize(self, document: CardDocument) -> dict[str, Any]:
        return {"_index": self._index_name, "_id": document.item.id, "_source": self.document_schema.dump(document)}
