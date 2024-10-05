from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from trading_journal.journal.models import Account
from trading_journal.journal.models import History
from trading_journal.journal.models import Position


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "broker", "balance")
    list_display_links = list_display
    readonly_fields = ("balance",)
    search_fields = ("name",)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("account", "operation", "created_at", "profit", "balance")
    list_display_links = ("account", "operation", "created_at", "profit", "balance")
    list_filter = ("account",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    autocomplete_fields = ("account",)
    list_display = (
        "account",
        "ticket",
        "symbol",
        "volume",
        "opened_at",
        "open_price",
        "closed_at",
        "close_price",
        "swaps",
        "profit",
    )
    list_display_links = list_display
    fieldsets = (
        (None, {"fields": ("account", "symbol", "volume")}),
        (_("Open"), {"fields": ("opened_at", "open_price")}),
        (_("Security"), {"fields": ("sl_price", "tp_price")}),
        (_("Close"), {"fields": ("closed_at", "close_price")}),
        (_("Swaps & commissions"), {"fields": ("commissions", "swaps")}),
        (_("Profit"), {"fields": ("profit",)}),
    )
