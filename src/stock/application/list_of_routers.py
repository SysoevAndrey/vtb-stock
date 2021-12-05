from stock.application.controllers import car_list_router
from stock.application.controllers import car_single_router
from fastapi_utils.inferring_router import InferringRouter


def get_routers() -> list[InferringRouter]:
    return [
        car_list_router,
        car_single_router,
    ]
