from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from trading_journal.core.models import OwnerModel
from trading_journal.journal.exceptions import (
    PositionAlreadyExistsError,
    PositionNotClosedError,
    TemporalDisturbanceError,
)
from trading_journal.journal.types import OperationType
from trading_journal.markets.models import Broker, Symbol


class Account(OwnerModel):
    name = models.CharField(_("Name"), max_length=300)
    broker = models.ForeignKey(
        Broker,
        verbose_name=_("Broker"),
        on_delete=models.PROTECT,
        related_name="accounts",
    )
    balance = models.DecimalField(
        _("Balance"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    currency = models.CharField(_("Currency"), max_length=3, default="USD")

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.name


class Position(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        related_name="positions",
    )
    ticket = models.PositiveBigIntegerField(_("Ticket no."))
    volume = models.DecimalField(_("Volume"), max_digits=10, decimal_places=4)
    symbol = models.ForeignKey(
        Symbol,
        verbose_name=_("Symbol"),
        on_delete=models.PROTECT,
        related_name="positions",
    )

    opened_at = models.DateTimeField(_("Opened at"), default=now)
    open_price = models.DecimalField(_("Open price"), max_digits=10, decimal_places=4)

    sl_price = models.DecimalField(
        _("Stop loss price"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )
    tp_price = models.DecimalField(
        _("Take profit price"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )

    closed_at = models.DateTimeField(_("Closed at"), blank=True, null=True)
    closed_manually = models.BooleanField(_("Closed manually"), blank=True, null=True)
    close_price = models.DecimalField(
        _("Close price"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )

    commissions = models.DecimalField(
        _("Commissions"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )
    swaps = models.DecimalField(
        _("Swaps"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )
    profit = models.DecimalField(
        _("Profit"),
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
    )

    modifications = models.JSONField(_("Modifications"), default=dict)

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")
        ordering = ["opened_at"]

    def __str__(self):
        return f"{self.ticket} @ {self.account.name}"


class History(models.Model):
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        related_name="history",
    )
    profit = models.DecimalField(
        _("Profit"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    balance = models.DecimalField(
        _("Balance"),
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    operation = models.CharField(_("Operation"), max_length=20, choices=OperationType)
    position = models.ForeignKey(
        Position,
        verbose_name=_("Position"),
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("Created at"))

    class Meta:
        verbose_name = _("History")
        verbose_name_plural = _("History")
        ordering = ["created_at"]
        constraints = [
            UniqueConstraint(
                fields=["account", "position"],
                name="unique_position",
                condition=Q(position__isnull=False),
            ),
        ]

    def __str__(self):
        return f"{self.created_at} @ {self.account.name}"

    @classmethod
    def add_closed_position(cls, position: Position, *, force=False):
        if position.closed_at is None:
            raise PositionNotClosedError

        if cls.objects.filter(account=position.account, position=position).exists():
            raise PositionAlreadyExistsError

        last_one = cls.objects.filter(account=position.account).order_by("-created_at").first()

        if not force and last_one and last_one.created_at > position.closed_at:
            raise TemporalDisturbanceError

        profit = position.profit + position.swaps - position.commissions

        row = cls.objects.create(
            account=position.account,
            position=position,
            operation=OperationType.POSITION_CLOSE,
            created_at=position.closed_at,
            profit=profit,
            balance=profit + (last_one.balance if last_one else 0),
        )

        position.account.balance = row.balance
        position.account.save(update_fields=["balance"])

        return row

    @classmethod
    def add_row(
        cls,
        account: Account,
        profit: float | Decimal,
        operation_type: OperationType,
        created_at: datetime | None = None,
        *,
        force=False,
    ):
        last_one = cls.objects.filter(account=account).order_by("-created_at").first()
        new_created_at = created_at or now()

        if not force and last_one and last_one.created_at > new_created_at:
            raise TemporalDisturbanceError

        row = cls.objects.create(
            account=account,
            operation=operation_type,
            created_at=new_created_at,
            profit=profit,
            balance=profit + (last_one.balance if last_one else 0),
        )

        account.balance = row.balance
        account.save(update_fields=["balance"])

        return row

    @classmethod
    def recalculate_balance(cls, account: Account):
        balance = 0

        for row in cls.objects.filter(account=account).order_by("created_at").all():
            balance += row.profit
            row.balance = balance
            row.save(update_fields=["balance"])

        account.balance = balance
        account.save(update_fields=["balance"])
