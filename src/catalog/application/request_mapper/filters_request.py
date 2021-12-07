from typing import Any, Optional

from marshmallow import fields, pre_load
from marshmallow_enum import EnumField
from pydantic import BaseModel, Field

from catalog.application.request_mapper import RequestSchema
from catalog.core.domain.available_parameter import ParameterType


class SelectedInterval(BaseModel):
    gte: float
    lte: float


class SelectedParameter(BaseModel):
    id: str
    type: ParameterType
    selected_values: list[str]
    selected_interval: Optional[SelectedInterval]


class FiltersRequest(BaseModel):
    categories: list[str] = Field(default_factory=list)
    sort: list[str] = Field(default_factory=list)
    parameters: list[SelectedParameter] = Field(default_factory=list)
    search: Optional[str] = Field(default=None)
    page: int = Field(default=1)
    size: int = Field(default=10)


class SelectedIntervalRequestSchema(RequestSchema):
    __model__ = SelectedInterval
    gte = fields.Float()
    lte = fields.Float()


class SelectedParameterRequestSchema(RequestSchema):
    __model__ = SelectedParameter.construct
    id = fields.String()
    type = EnumField(ParameterType, by_value=True)
    selected_values = fields.List(fields.String())
    selected_interval = fields.Nested(SelectedIntervalRequestSchema, missing=None, allow_none=True)


class FiltersRequestSchema(RequestSchema):
    __model__ = FiltersRequest.construct
    categories = fields.List(fields.String())
    sort = fields.List(fields.String())
    parameters = fields.List(fields.Nested(SelectedParameterRequestSchema))
    search = fields.String(allow_none=True, missing=None)
    page = fields.Integer()
    size = fields.Integer()

    @pre_load
    def prepare_request_data(self, data: dict[str, Any], **kwargs) -> dict[str, Any]:
        print(data)
        parameters = self._prepare_parameters(data["filters"])
        return {**data, "parameters": parameters}

    @staticmethod
    def _prepare_parameters(parameters: list[str]) -> list[dict[str, Any]]:
        result_parameters: dict[str, dict[str, Any]] = {}
        for parameter in parameters:
            identifier, value = parameter.split("=")
            type_ = (
                ParameterType.NUMBER
                if identifier.startswith("max") or identifier.startswith("min")
                else ParameterType.KEYWORD
            )
            selected_values = []
            prefix = None
            if identifier.startswith("max"):
                prefix = "max"
                identifier = identifier.removeprefix(prefix).lower()
            if identifier.startswith("min"):
                prefix = "min"
                identifier = identifier.removeprefix(prefix).lower()
            if not result_parameters.get(identifier):
                result_parameters[identifier] = dict(id=identifier, type=type_.value)
            if type_ is ParameterType.KEYWORD:
                selected_values.extend(value.split(";"))
                result_parameters[identifier].update(selected_values=selected_values, selected_interval=None)
            elif prefix == "min":
                result_parameters[identifier].update(
                    selected_values=[],
                    selected_interval=dict(
                        gte=float(value), lte=result_parameters[identifier].get("selected_interval", {}).get("lte")
                    ),
                )
            elif prefix == "max":
                result_parameters[identifier].update(
                    selected_values=[],
                    selected_interval=dict(
                        gte=result_parameters[identifier].get("selected_interval", {}).get("gte"), lte=float(value)
                    ),
                )
        return list(result_parameters.values())
