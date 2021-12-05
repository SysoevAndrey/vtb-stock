from uuid import UUID

import aiohttp
from gateway.core.domain.payment import Payment
from gateway.infrastructure.gateways.loaders.payment_schema import PaymentLoaderSchema


class PaymentsAdapter:
    payment_single_schema = PaymentLoaderSchema()

    def __init__(self, host: str):
        self._host = host
        self._payments_api = f"{host}/api/payments"

    async def get_payment_by_id(self, payment_id: UUID) -> Payment:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._payments_api}/{payment_id}") as resp:
                resp.raise_for_status()
                return self.payment_single_schema.load(await resp.json())

    async def decline_payment(self, payment_id: UUID):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self._payments_api}/{payment_id}") as resp:
                resp.raise_for_status()
                await resp.read()

    async def save_payment_info(self, price: int) -> Payment:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._payments_api}", json={"price": price}) as resp:
                resp.raise_for_status()
                return self.payment_single_schema.load(await resp.json())
