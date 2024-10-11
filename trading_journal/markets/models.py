from functools import cached_property

from django.db import models
from django.utils.translation import gettext_lazy as _

from trading_journal.core.helpers import get_joined_m2m_names


class Market(models.Model):
    """
    Market Model

    This model represents a market with a name attribute.

    Attributes:
        name (CharField): The name of the market. It has a maximum length of 50 characters.

    Meta:
        verbose_name (str): The singular name for a market.
        verbose_name_plural (str): The plural name for markets.

    Methods:
        __str__: Returns the name of the market.
    """

    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Market")
        verbose_name_plural = _("Markets")

    def __str__(self):
        return self.name


class Broker(models.Model):
    """
    Represents a Broker in the system. Brokers can be associated
    with multiple markets.

    Attributes:
        name (CharField): The name of the broker, with a maximum length of 300 characters.
        markets (ManyToManyField): A many-to-many relationship to the Market model. This field is optional
        (can be blank) and relates back to brokers via the related name 'brokers'.

    Meta:
        verbose_name: The human-readable name of the model in singular form.
        verbose_name_plural: The human-readable name of the model in plural form.

    Methods:
        __str__: Returns the name of the broker.
        markets_names: Returns a comma-separated string of the names of the markets associated with the broker.
    """

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
    """
    A Django model representing different types of symbols.

    The `SymbolType` model provides a way to classify and manage symbol categories in the application.

    Attributes:
        name (CharField): The unique name of the symbol type with a maximum length of 50 characters.

    Methods:
        __str__(): Returns the name of the symbol type.
    """

    name = models.CharField(_("Name"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("Symbol Type")
        verbose_name_plural = _("Symbol Types")

    def __str__(self):
        return self.name


class Symbol(models.Model):
    """
    Represents a financial symbol such as a stock ticker.

    Attributes
    ----------
    name : CharField
        The name of the financial symbol.
    code : CharField
        A short code representing the financial symbol.
    type : ForeignKey to SymbolType
        The type of financial symbol (e.g., stock, bond).
    brokers : ManyToManyField to Broker
        The brokers associated with the financial symbol.
    market : ForeignKey to Market
        The market in which the financial symbol is traded.

    Meta
    ----
    verbose_name : str
        The human-readable name for the object, "Symbol".
    verbose_name_plural : str
        The plural form of the human-readable name, "Symbols".
    unique_together : tuple
        Ensures that the combination of code and market is unique.

    Methods
    -------
    __str__()
        Returns the name of the financial symbol.
    brokers_names() -> str
        Returns a comma-separated list of broker names associated with the symbol.
    """

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
