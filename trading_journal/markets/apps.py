from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketsConfig(AppConfig):
    """
    MarketsConfig is a Django application configuration class for the 'Markets' application.

    name:
        The full Python path to the application.

    verbose_name:
        A human-readable name for the application.
    """

    name = "trading_journal.markets"
    verbose_name = _("Markets")
