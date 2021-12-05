from typing import Any, Callable

from marshmallow import EXCLUDE, Schema, post_load


class LoaderSchema(Schema):
    __model__: Callable[..., Any] = None  # type: ignore

    class Meta:
        ordered = True
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
