from payment.application.controllers import payment_single_router
from payment.application.controllers import payment_list_router
from fastapi_utils.inferring_router import InferringRouter


def get_routers() -> list[InferringRouter]:
    return [
        payment_single_router,
        payment_list_router,
    ]
