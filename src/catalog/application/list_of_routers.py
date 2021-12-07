from fastapi_utils.inferring_router import InferringRouter
from catalog.application.controllers import card_list_router, filters_list_router


def get_routers() -> list[InferringRouter]:
    return [
        card_list_router,
        filters_list_router,
    ]
