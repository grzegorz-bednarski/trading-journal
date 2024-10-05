from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class OperationType(TextChoices):
    DEPOSIT = "DE", _("Deposit")
    DIVIDENDS = "DI", _("Dividends")
    POSITION_CLOSE = "PC", _("Position Close")
    WITHDRAWAL = "WD", _("Withdrawal")
