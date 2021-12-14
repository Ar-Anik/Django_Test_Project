from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse_lazy

DEFAULT_SETTINGS = {
    "default_store": {},
   # "success_url": reverse_lazy('home'),
   # "fail_url": reverse_lazy('cart'),
   # "cancel_url": reverse_lazy('home'),

    "success_url": reverse_lazy('home'),
    "fail_url": reverse_lazy('my-orders'),
    "cancel_url": reverse_lazy('my-orders'),

    "success_template_name": "django_sslcommerz/common-alert.html",
    "fail_template_name": "django_sslcommerz/common-alert.html",
    "cancel_template_name": "django_sslcommerz/common-alert.html",
    "error_template_name": "django_sslcommerz/common-alert.html",
    "session_keys_to_serialize": ("tran_id", "status"),
}

app_settings = {**DEFAULT_SETTINGS, **getattr(settings, "DJANGO_SSLCOMMERZ", {})}


class DjangoSslcommerzConfig(AppConfig):
    name = "django_sslcommerz"
