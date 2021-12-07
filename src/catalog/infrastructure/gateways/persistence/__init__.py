from typing import Any, Callable, Optional
from marshmallow import EXCLUDE
from marshmallow import post_load
from marshmallow import Schema


class PersistenceSchema(Schema):
    __model__: Optional[Callable[..., Any]] = None

    class Meta:
        ordered = True
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs):
        if self.__model__:
            return self.__model__(**data)
        return data
