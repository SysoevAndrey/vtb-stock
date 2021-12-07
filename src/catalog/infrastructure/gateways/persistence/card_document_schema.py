from marshmallow import fields

from catalog.core.domain.card_document import CardCategory, CardDocument, KeywordParameter, NumberParameter
from catalog.infrastructure.gateways.persistence import PersistenceSchema


class NumberParameterPersistenceSchema(PersistenceSchema):
    __model__ = NumberParameter

    id = fields.String(load_only=True)
    value = fields.Float(load_only=True)

    facet_info = fields.String(dump_only=True)
    facet_value = fields.String(dump_only=True)


class KeywordParameterPersistenceSchema(PersistenceSchema):
    __model__ = KeywordParameter

    id = fields.String(load_only=True)
    values = fields.List(fields.String(), load_only=True)

    facet_info = fields.String(dump_only=True)
    facet_value = fields.String(dump_only=True)


class CardCategoryPersistenceSchema(PersistenceSchema):
    __model__ = CardCategory
    paths = fields.List(fields.String())


class CardDocumentPersistenceSchema(PersistenceSchema):
    __model__ = CardDocument

    type = fields.String()
    number_parameters = fields.List(fields.Nested(NumberParameterPersistenceSchema))
    keyword_parameters = fields.List(fields.Nested(KeywordParameterPersistenceSchema))
    category = fields.Nested(CardCategoryPersistenceSchema)

    search_result = fields.Dict(fields.String(), fields.String(), dump_only=True)
    number_search_data = fields.Dict(fields.String(), fields.Float(), dump_only=True)
    keyword_search_data = fields.Dict(fields.String(), fields.List(fields.String()), dump_only=True)
