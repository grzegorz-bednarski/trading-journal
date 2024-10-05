from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketsConfig(AppConfig):
    name = "trading_journal.markets"
    verbose_name = _("Markets")
