import inject
from stock.application.controllers.api_router import get_api_router
from stock.application.presentation.car_list_response import (
    CarListResponse,
    CarListResponsePresentationSchema,
    CarResponse,
    CarResponsePresentationSchema,
)
from stock.application.request_mapper.create_car_request import CreateCarRequest
from stock.core.services.car_list_service import CarListService
from fastapi.params import Query
from fastapi_utils.cbv import cbv
from pydantic import BaseConfig
from starlette.status import HTTP_201_CREATED

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class CarListResource:
    car_list_response_schema = CarListResponsePresentationSchema()
    car_response_schema = CarResponsePresentationSchema()

    @router.get(
        "/api/cars",
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
        service = inject.instance(CarListService)
        cars_result = await service.show_cars(page=page, size=size, show_all=show_all)
        return self.car_list_response_schema.dump(
            {"page_size": len(cars_result.cars), "page": page, "result": cars_result}
        )

    @router.post("/api/cars", status_code=HTTP_201_CREATED, response_model=CarResponse)
    async def save_car(self, car: CreateCarRequest):
        service = inject.instance(CarListService)
        created_car = await service.save_car(car)
        return self.car_response_schema.dump(created_car)
