from dataclasses import asdict
import json
from marshmallow import fields

from catalog.core.domain.card_document import (
    CardCategory,
    CardDocument,
    FacetedParameter,
    KeywordParameter,
    NumberParameter,
)
from catalog.infrastructure.gateways.persistence import PersistenceSchema


class FacetedParameterPersistenceSchema(PersistenceSchema):
    id = fields.String()
    label = fields.String()

    facet_info = fields.Method("make_facet_info", dump_only=True)

    @staticmethod
    def make_facet_info(doc: FacetedParameter) -> str:
        return json.dumps({"id": doc.id, "label": doc.label})


class NumberParameterPersistenceSchema(FacetedParameterPersistenceSchema):
    __model__ = NumberParameter

    value = fields.Float()


class KeywordParameterPersistenceSchema(FacetedParameterPersistenceSchema):
    __model__ = KeywordParameter

    values = fields.List(fields.String())

    facet_value = fields.Method("make_facet_value", dump_only=True)

    @staticmethod
    def make_facet_value(doc: KeywordParameter) -> list[str]:
        return [json.dumps({"id": value, "label": value}) for value in doc.values]


class CardCategoryPersistenceSchema(PersistenceSchema):
    __model__ = CardCategory
    id = fields.String()
    parent = fields.String(allow_none=True)
    image = fields.String()
    label = fields.String()

    facet_info = fields.Method("make_facet_info", dump_only=True)

    @staticmethod
    def make_facet_info(doc: CardCategory) -> str:
        return json.dumps({"id": doc.id, "label": doc.label, "parent": doc.parent, "image": doc.image})


class CardDocumentPersistenceSchema(PersistenceSchema):
    __model__ = CardDocument

    type = fields.String()
    number_parameters = fields.List(fields.Nested(NumberParameterPersistenceSchema))
    keyword_parameters = fields.List(fields.Nested(KeywordParameterPersistenceSchema))
    number_sort_parameters = fields.List(fields.Nested(NumberParameterPersistenceSchema))
    categories = fields.List(fields.Nested(CardCategoryPersistenceSchema))

    categories_navigation = fields.Method("make_categories_navigation", dump_only=True)
    search_result = fields.Method("make_search_result", dump_only=True)
    number_search_data = fields.Method("make_number_search_data", dump_only=True)
    keyword_search_data = fields.Method("make_keyword_search_data", dump_only=True)
    sort_numbers_data = fields.Method("make_number_sort", dump_only=True)

    @staticmethod
    def make_number_sort(doc: CardDocument) -> dict[str, float]:
        return {parameter.id: parameter.value for parameter in doc.number_sort_parameters}

    @staticmethod
    def make_search_result(doc: CardDocument) -> dict[str, str]:
        return {key: str(value) for key, value in asdict(doc.item).items()}

    @staticmethod
    def make_categories_navigation(doc: CardDocument) -> dict[str, list[str] | str]:
        return {
            "path": [category.id for category in doc.categories],
            "direct_parent": doc.categories[-1].id,
        }

    @staticmethod
    def make_number_search_data(doc: CardDocument) -> dict[str, float]:
        return {parameter.id: parameter.value for parameter in doc.number_parameters}

    @staticmethod
    def make_keyword_search_data(doc: CardDocument) -> dict[str, list[str]]:
        return {parameter.id: parameter.values for parameter in doc.keyword_parameters}
