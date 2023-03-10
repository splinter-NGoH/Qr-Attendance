from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "qr_code.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import qr_code.users.signals  
        except ImportError:
            pass
