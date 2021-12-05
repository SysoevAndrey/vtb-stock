import inject
from fastapi.params import Header
from fastapi_utils.cbv import cbv
from pydantic import BaseConfig
from rental.application.controllers.api_router import get_api_router
from rental.application.presentation.rental_single_response import RentalResponse, RentalResponsePresentationSchema
from rental.application.request_mapper.create_rental_request import CreateRentalRequest
from rental.core.services.rental_list_service import RentalListService
from starlette.status import HTTP_201_CREATED

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class RentalListResource:
    rental_response_schema = RentalResponsePresentationSchema()

    @router.get(
        "/api/rental",
        response_model=list[RentalResponse],
        response_model_exclude_none=True,
        response_model_by_alias=True,
    )
    async def get_list_of_rentals(
        self, user_id: str = Header(..., alias="X-User-Name")  # type: ignore
    ) -> list[RentalResponse]:
        service = inject.instance(RentalListService)
        rentals_result = await service.show_rentals_for_user(user_id=user_id)
        return [self.rental_response_schema.dump(rental) for rental in rentals_result]

    @router.post("/api/rental", status_code=HTTP_201_CREATED, response_model=RentalResponse)
    async def save_rental(self, rental: CreateRentalRequest, user_id: str = Header(..., alias="X-User-Name")):  # type: ignore
        service = inject.instance(RentalListService)
        created_rental = await service.save_rental_for_user(rental, user_id=user_id)
        return self.rental_response_schema.dump(created_rental)
