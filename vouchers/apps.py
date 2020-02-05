from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VouchersConfig(AppConfig):
    name = "vouchers"
    verbose_name = _("Vouchers")

    def ready(self):
        try:
            import vouchers.signals  # noqa F401
        except ImportError:
            pass
