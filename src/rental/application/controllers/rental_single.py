import inject
from fastapi.params import Header, Path
from fastapi_utils.cbv import cbv
from pydantic import BaseConfig
from pydantic.types import UUID4
from rental.application.controllers.api_router import get_api_router
from rental.application.presentation.errors import NotFoundError
from rental.application.presentation.rental_single_response import RentalResponse, RentalResponsePresentationSchema
from rental.core.services.rental_list_service import RentalListService
from starlette import status
from starlette.responses import JSONResponse, Response

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class RentalSingleResource:
    rental_response_schema = RentalResponsePresentationSchema()

    @router.get(
        "/api/rental/{rentalUid}",
        response_model=RentalResponse,
        response_model_exclude_none=True,
        response_model_by_alias=True,
        responses={"200": {"model": RentalResponse}, "404": {"model": NotFoundError}},
    )
    async def get_rental_for_user(
        self,
        user_id: str = Header(..., alias="X-User-Name"),  # type: ignore
        rental_uid: UUID4 = Path(..., alias="rentalUid"),  # type: ignore
    ) -> list[RentalResponse] | JSONResponse:
        service = inject.instance(RentalListService)
        rental_result = await service.show_rental_for_user(user_id=user_id, rental_id=rental_uid)
        if rental_result:
            return self.rental_response_schema.dump(rental_result)
        return JSONResponse(
            {"message": f"Rental - '{rental_uid}' for user - '{user_id}' was not found."}, status_code=404
        )

    @router.delete(
        "/api/rental/{rentalUid}",
        responses={"204": {"status_code": status.HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def decline_rental_for_user(
        self,
        user_id: str = Header(..., alias="X-User-Name"),  # type: ignore
        rental_uid: UUID4 = Path(..., alias="rentalUid"),  # type: ignore
    ):
        service = inject.instance(RentalListService)
        rental_result = await service.decline_rental_for_user(user_id=user_id, rental_uid=rental_uid)
        if rental_result:
            return Response(b"", status_code=status.HTTP_204_NO_CONTENT)
        else:
            return JSONResponse(
                {"message": f"Rental - '{rental_uid}' for user - '{user_id}' was not found."}, status_code=404
            )

    @router.post(
        "/api/rental/{rentalUid}/finish",
        responses={"204": {"status_code": status.HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def finish_rental_for_user(
        self,
        user_id: str = Header(..., alias="X-User-Name"),  # type: ignore
        rental_uid: UUID4 = Path(..., alias="rentalUid"),  # type: ignore
    ):
        service = inject.instance(RentalListService)
        rental_result = await service.finish_rental_for_user(user_id=user_id, rental_uid=rental_uid)
        if rental_result:
            return Response(b"", status_code=status.HTTP_204_NO_CONTENT)
        else:
            return JSONResponse(
                {"message": f"Rental - '{rental_uid}' for user - '{user_id}' was not found."}, status_code=404
            )

    @router.post(
        "/api/rental/{rentalUid}/start",
        responses={"204": {"status_code": status.HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def start_rental_for_user(
        self,
        user_id: str = Header(..., alias="X-User-Name"),  # type: ignore
        rental_uid: UUID4 = Path(..., alias="rentalUid"),  # type: ignore
    ):
        service = inject.instance(RentalListService)
        rental_result = await service.start_rental_for_user(user_id=user_id, rental_uid=rental_uid)
        if rental_result:
            return Response(b"", status_code=status.HTTP_204_NO_CONTENT)
        else:
            return JSONResponse(
                {"message": f"Rental - '{rental_uid}' for user - '{user_id}' was not found."}, status_code=404
            )
