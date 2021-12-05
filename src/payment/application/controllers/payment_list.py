import inject
from fastapi_utils.cbv import cbv
from payment.application.controllers.api_router import get_api_router
from payment.application.presentation.payment_single_response import PaymentResponse, PaymentResponsePresentationSchema
from payment.application.request_mapper.create_payment_request import CreatePaymentRequest
from payment.core.services.payment_list_service import PaymentListService
from pydantic import BaseConfig

BaseConfig.arbitrary_types_allowed = True

router = get_api_router()


@cbv(router)
class PaymentListResource:
    payment_response_schema = PaymentResponsePresentationSchema()

    @router.post(
        "/api/payments", response_model=PaymentResponse, response_model_exclude_none=True, response_model_by_alias=True
    )
    async def apply_payment(self, payment_request: CreatePaymentRequest) -> PaymentResponse:
        service = inject.instance(PaymentListService)
        payment_result = await service.save_payment(payment_request=payment_request)
        return self.payment_response_schema.dump(payment_result)
