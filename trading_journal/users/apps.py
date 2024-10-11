import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """
    UsersConfig is a Django application configuration class for the 'users' app.

    Attributes:
    name (str): The full Python path to the application.
    verbose_name (str): A human-readable name for the application.

    Methods:
    ready(self): Method called when the application is ready.
        It attempts to import the 'signals' module. If the module cannot be imported,
        it suppresses the ImportError.
    """

    name = "trading_journal.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import trading_journal.users.signals  # noqa: F401
