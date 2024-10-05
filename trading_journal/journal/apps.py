from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketsConfig(AppConfig):
    name = "trading_journal.journal"
    verbose_name = _("Journal")
