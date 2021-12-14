from .store import SslcommerzStore

from .apps import app_settings
from .mainhandlers import DjangoPaymentHandler

default_store_config = app_settings["default_store"]
default_store = SslcommerzStore(**default_store_config)
payment_handler = DjangoPaymentHandler(store=default_store)
