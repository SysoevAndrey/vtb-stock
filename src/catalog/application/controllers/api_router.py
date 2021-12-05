from fastapi_utils.inferring_router import InferringRouter


def get_api_router(**kwargs) -> InferringRouter:
    return InferringRouter(**kwargs)
