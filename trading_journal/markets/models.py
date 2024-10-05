from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _

from trading_journal.core.helpers import get_joined_m2m_names


class Market(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Market")
        verbose_name_plural = _("Markets")

    def __str__(self):
        return self.name


class Broker(models.Model):
    name = models.CharField(_("Name"), max_length=300)
    markets = models.ManyToManyField(
        Market,
        verbose_name=_("Markets"),
        blank=True,
        related_name="brokers",
    )

    class Meta:
        verbose_name = _("Broker")
        verbose_name_plural = _("Brokers")

    def __str__(self):
        return self.name

    @cached_property
    def markets_names(self) -> str:
        return get_joined_m2m_names(self, "markets")


class SymbolType(models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("Symbol Type")
        verbose_name_plural = _("Symbol Types")

    def __str__(self):
        return self.name


class Symbol(models.Model):
    name = models.CharField(_("Name"), max_length=300)
    code = models.CharField(_("Code"), max_length=15)
    type = models.ForeignKey(
        SymbolType,
        verbose_name=_("Type"),
        on_delete=models.CASCADE,
        related_name="symbols",
    )
    brokers = models.ManyToManyField(
        Broker,
        verbose_name=_("Brokers"),
        blank=True,
        related_name="symbols",
    )
    market = models.ForeignKey(
        Market,
        verbose_name=_("Market"),
        related_name="symbols",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Symbol")
        verbose_name_plural = _("Symbols")
        unique_together = (("code", "market"),)

    def __str__(self):
        return self.name

    @cached_property
    def brokers_names(self) -> str:
        return get_joined_m2m_names(self, "brokers")
