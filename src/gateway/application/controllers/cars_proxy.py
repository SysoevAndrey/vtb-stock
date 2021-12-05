import inject
from fastapi import Query
from fastapi_utils.cbv import cbv
from gateway.application.controllers.api_router import get_api_router
from gateway.application.presentation.car_list_response import (
    CarListResponse,
    CarListResponsePresentationSchema,
    CarResponsePresentationSchema,
)
from gateway.core.services.car_proxy_service import CarProxyService

router = get_api_router()


@cbv(router)
class CarsProxyRouter:
    car_list_response_schema = CarListResponsePresentationSchema()
    car_response_schema = CarResponsePresentationSchema()

    @router.get(
        "/api/v1/cars",
        response_model=CarListResponse,
        response_model_exclude_none=True,
        response_model_by_alias=True,
    )
    async def get_list_of_cars(
        self,
        page: int = Query(default=1, alias="page"),  # type: ignore
        size: int = Query(default=10, alias="size"),  # type: ignore
        show_all: bool = Query(default=False, alias="showAll"),  # type: ignore
    ) -> CarListResponse:
        service = inject.instance(CarProxyService)
        cars_result = await service.list_of_cars(page=page, size=size, show_all=show_all)
        return self.car_list_response_schema.dump(cars_result)
