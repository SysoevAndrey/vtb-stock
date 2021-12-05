from functools import partial
from time import sleep

import inject
from catalog.entrypoint.config import Config

def _configure(inject_binder: inject.Binder, config: Config):
    inject_binder.bind(Config, config)


def bind(config: Config):
    inject.configure_once(partial(_configure, config=config))
    if not config.is_debug:
        # Wait for injector
        sleep(10)
