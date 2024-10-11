from django.contrib import admin

from trading_journal.markets.models import Broker, Market, Symbol, SymbolType


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("markets",)
    list_display = ("pk", "name", "markets_names")
    list_display_links = list_display
    search_fields = ("name",)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = list_display
    search_fields = ("name",)


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    autocomplete_fields = ("brokers", "market")
    list_display = ("pk", "name", "code", "type", "market")
    list_display_links = list_display
    list_filter = ("type", "market")
    search_fields = ("name", "code")


@admin.register(SymbolType)
class SymbolTypeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    list_display_links = list_display
    search_fields = ("name",)
