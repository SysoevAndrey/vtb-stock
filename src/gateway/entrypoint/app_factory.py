from typing import Type

from gateway.application import get_error_handlers, get_routers
from gateway.entrypoint.bindings import bind
from gateway.entrypoint.config import Config
from fastapi import FastAPI


def _register_server_error_handlers(app: FastAPI):
    for handler in get_error_handlers():
        app.exception_handler(Exception)(handler)


def _build_http_api(app: FastAPI):
    for router in get_routers():
        app.include_router(router)


def create_app(config_cls: Type[Config] = Config) -> FastAPI:
    config_obj = config_cls()
    app = FastAPI()
    bind(config_obj)
    _build_http_api(app)
    _register_server_error_handlers(app)
    return app
