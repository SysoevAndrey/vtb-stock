from fastapi_utils.inferring_router import InferringRouter
from gateway.application.controllers import cars_proxy_router, rental_proxy_router


def get_routers() -> list[InferringRouter]:
    return [
        rental_proxy_router,
        cars_proxy_router,
    ]
