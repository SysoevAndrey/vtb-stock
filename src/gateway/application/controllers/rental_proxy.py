import inject
from fastapi.params import Header, Path
from fastapi_utils.cbv import cbv
from starlette.responses import Response
from gateway.application.controllers.api_router import get_api_router
from gateway.application.presentation.errors import NotFoundError
from gateway.application.presentation.rental_response import (
    PayedRentalResponse,
    PayedRentalResponsePresnetationSchema,
    RentalResponse,
    RentalResponsePresentationSchema,
)
from gateway.application.request_mapper.create_rental_request import CreateRentalRequest
from gateway.core.services.rental_proxy_service import RentalProxyService
from pydantic.types import UUID4
from starlette.status import HTTP_204_NO_CONTENT

router = get_api_router()


@cbv(router)
class RentalProxyResource:
    rental_response_schema = RentalResponsePresentationSchema()
    payed_rental_schema = PayedRentalResponsePresnetationSchema()

    @router.get(
        "/api/v1/rental",
        response_model=list[RentalResponse],
        response_model_by_alias=True,
        response_model_exclude_none=True,
    )
    async def get_all_rentals_for_user(self, user_id: str = Header(..., alias="X-User-Name")) -> RentalResponse:  # type: ignore
        service = inject.instance(RentalProxyService)

        response = await service.get_assembled_rentals(user_id)

        return self.rental_response_schema.dump(response, many=True)

    @router.get(
        "/api/v1/rental/{rentalUid}",
        response_model=RentalResponse,
        response_model_by_alias=True,
        response_model_exclude_none=True,
        responses={"200": {"model": RentalResponse}, "404": {"model": NotFoundError}},
    )
    async def get_rental_for_user(self, user_id: str = Header(..., alias="X-User-Name"), rental_id: UUID4 = Path(..., alias="rentalUid")):  # type: ignore
        service = inject.instance(RentalProxyService)

        response = await service.get_assembled_rental(user_id, rental_id)

        return self.rental_response_schema.dump(response)

    @router.post(
        "/api/v1/rental",
        response_model=PayedRentalResponse,
        response_model_by_alias=True,
        response_model_exclude_none=True,
    )
    async def apply_rental(self, rental_request: CreateRentalRequest, user_id: str = Header(..., alias="X-User-Name")):  # type: ignore
        service = inject.instance(RentalProxyService)

        rental_proj, payment = await service.apply_rental(user_id, rental_request)

        return self.payed_rental_schema.dump({**rental_proj.dict(), "payment": payment})

    @router.delete(
        "/api/v1/rental/{rentalUid}",
        responses={"204": {"status_code": HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def decline_rental(self, user_id: str = Header(..., alias="X-User-Name"), rental_id: UUID4 = Path(..., alias="rentalUid")):  # type: ignore
        service = inject.instance(RentalProxyService)

        await service.cancel_rental(user_id, rental_id)
        return Response(b"", status_code=HTTP_204_NO_CONTENT)

    @router.post(
        "/api/v1/rental/{rentalUid}/finish",
        responses={"204": {"status_code": HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def finish_rental(self, user_id: str = Header(..., alias="X-User-Name"), rental_id: UUID4 = Path(..., alias="rentalUid")):  # type: ignore
        service = inject.instance(RentalProxyService)

        await service.finish_rental(user_id, rental_id)
        return Response(b"", status_code=HTTP_204_NO_CONTENT)
