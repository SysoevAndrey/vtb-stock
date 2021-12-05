from functools import partial
from time import sleep

import inject
from gateway.core.services.car_proxy_service import CarProxyService
from gateway.core.services.rental_proxy_service import RentalProxyService
from gateway.entrypoint.config import Config
from gateway.infrastructure.gateways.cars_adapter import CarsAdapter
from gateway.infrastructure.gateways.payments_adapter import PaymentsAdapter
from gateway.infrastructure.gateways.rentals_adapter import RentalsAdapter


def _configure(inject_binder: inject.Binder, config: Config):
    inject_binder.bind(Config, config)

    payments_adapter = PaymentsAdapter(host=config.payments_host)
    rentals_adapter = RentalsAdapter(host=config.rentals_host)
    cars_adapter = CarsAdapter(host=config.cars_host)

    inject_binder.bind(PaymentsAdapter, payments_adapter)
    inject_binder.bind(RentalsAdapter, rentals_adapter)
    inject_binder.bind(CarsAdapter, cars_adapter)

    inject_binder.bind_to_constructor(CarProxyService, CarProxyService)  # type: ignore
    inject_binder.bind_to_constructor(RentalProxyService, RentalProxyService)  # type: ignore


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
