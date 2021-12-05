from rental.application.controllers import rental_list_router, rental_single_router
from fastapi_utils.inferring_router import InferringRouter


def get_routers() -> list[InferringRouter]:
    return [
        rental_list_router,
        rental_single_router,
    ]
