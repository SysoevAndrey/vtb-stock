from typing import Any, Callable, Optional

from marshmallow import Schema, post_load
from marshmallow.utils import EXCLUDE
from pydantic.main import BaseModel


class RequestSchema(Schema):
    __model__: Optional[Callable[..., BaseModel]] = None

    @post_load
    def make_model(self, data: dict[str, Any], **kwargs):
        if self.__model__:
            return self.__model__(**data)
        return data

    class Meta:
        unknown = EXCLUDE
