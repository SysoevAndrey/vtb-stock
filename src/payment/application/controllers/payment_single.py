import inject
from fastapi.params import Path
from fastapi_utils.cbv import cbv
from pydantic import BaseConfig
from pydantic.types import UUID4
from payment.application.controllers.api_router import get_api_router
from payment.application.presentation.errors import NotFoundError
from payment.application.presentation.payment_single_response import PaymentResponse, PaymentResponsePresentationSchema
from payment.core.services.payment_list_service import PaymentListService
from starlette import status
from starlette.responses import JSONResponse, Response

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class PaymentSingleResource:
    payment_response_schema = PaymentResponsePresentationSchema()

    @router.delete(
        "/api/payments/{paymentUid}",
        responses={"204": {"status_code": status.HTTP_204_NO_CONTENT}, "404": {"model": NotFoundError}},
    )
    async def decline_payment(
        self,
        payment_uid: UUID4 = Path(..., alias="paymentUid"),  # type: ignore
    ):
        service = inject.instance(PaymentListService)
        payment_result = await service.decline_payment(payment_id=payment_uid)
        if payment_result:
            return Response(b"", status_code=status.HTTP_204_NO_CONTENT)
        else:
            return JSONResponse({"message": f"Payment - '{payment_uid}' was not found."}, status_code=404)

    @router.get(
        "/api/payments/{paymentUid}",
        responses={"200": {"model": PaymentResponse}, "404": {"model": NotFoundError}},
    )
    async def get_payment_by_id(
        self,
        payment_uid: UUID4 = Path(..., alias="paymentUid"),  # type: ignore
    ):
        service = inject.instance(PaymentListService)
        payment_result = await service.get_payment_by_id(payment_id=payment_uid)
        if payment_result:
            return self.payment_response_schema.dump(payment_result)
        else:
            return JSONResponse({"message": f"Payment - '{payment_uid}' was not found."}, status_code=404)
