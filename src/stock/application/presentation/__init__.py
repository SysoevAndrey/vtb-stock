from typing import Callable, Optional

from marshmallow import Schema
from marshmallow.decorators import post_dump
from marshmallow.utils import INCLUDE
from pydantic.main import BaseModel


class PresentationSchema(Schema):
    __model__: Optional[Callable[..., BaseModel]] = None

    class Meta:
        ordered = True
        unknown = INCLUDE

    @post_dump
    def make_model(self, data, **kwargs):
        return self.__model__(**data)  # type: ignore
