import inject
from stock.application.controllers.api_router import get_api_router
from stock.application.presentation.car_list_response import CarResponse, CarResponsePresentationSchema
from stock.application.presentation.errors import NotFoundError
from stock.core.services.car_list_service import CarListService
from fastapi.params import Path
from fastapi_utils.cbv import cbv
from pydantic import BaseConfig
from pydantic.types import UUID4
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class CarSingleResource:
    car_schema = CarResponsePresentationSchema()

    @router.patch(
        "/api/cars/{carUid}/reserve",
        responses={"204": {"status_code": HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def reserve_car(self, car_uid: UUID4 = Path(..., alias="carUid")):  # type: ignore
        service = inject.instance(CarListService)
        reserved_car = await service.reserve_car(car_uid)
        if reserved_car:
            return Response(b"", status_code=HTTP_204_NO_CONTENT)
        return JSONResponse(content={"message": f"Car - '{car_uid}' was not found."}, status_code=HTTP_404_NOT_FOUND)

    @router.patch(
        "/api/cars/{carUid}/free",
        responses={"204": {"status_code": HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def free_car(self, car_uid: UUID4 = Path(..., alias="carUid")):  # type: ignore
        service = inject.instance(CarListService)
        reserved_car = await service.free_car(car_uid)
        if reserved_car:
            return Response(b"", status_code=HTTP_204_NO_CONTENT)
        return JSONResponse(content={"message": f"Car - '{car_uid}' was not found."}, status_code=HTTP_404_NOT_FOUND)

    @router.get(
        "/api/cars/{carUid}",
        responses={"200": {"model": CarResponse}, "404": {"model": NotFoundError}},
    )
    async def get_car_by_id(self, car_uid: UUID4 = Path(..., alias="carUid")):  # type: ignore
        service = inject.instance(CarListService)
        car = await service.get_car_by_id(car_uid)
        if car:
            return self.car_schema.dump(car)
        return JSONResponse(content={"message": f"Car - '{car_uid}' was not found."}, status_code=HTTP_404_NOT_FOUND)
