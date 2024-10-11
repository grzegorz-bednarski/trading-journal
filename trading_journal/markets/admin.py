from django.contrib import admin

from trading_journal.markets.models import Broker, Market, Symbol, SymbolType


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    """
    Django Admin class for managing Broker model.

    This class customizes the Django Admin interface for the Broker model by:

    - Enabling autocomplete for the 'markets' field.
    - Displaying 'pk', 'name', and 'markets_names' in the list view.
    - Making 'pk', 'name', and 'markets_names' clickable in the list view.
    - Adding a search field for 'name'.

    Attributes:
        autocomplete_fields (tuple): Specifies 'markets' field for autocomplete.
        list_display (tuple): Fields to display in the admin list view.
        list_display_links (tuple): Fields that should be clickable in the admin list view.
        search_fields (tuple): Fields that are searchable in the admin interface.
    """

    autocomplete_fields = ("markets",)
    list_display = ("pk", "name", "markets_names")
    list_display_links = list_display
    search_fields = ("name",)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    """
    Registers the Market model with the Django admin interface, allowing for its management through the Django
    admin site.

    Class:
        MarketAdmin: Defines the options and configuration for displaying the Market model in the admin interface.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view in the admin.
        list_display_links (tuple): Specifies which fields in list_display should be clickable links.
        search_fields (tuple): Specifies which fields should be searchable in the search box.
    """

    list_display = ("pk", "name")
    list_display_links = list_display
    search_fields = ("name",)


@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    """
    SymbolAdmin class customizes the admin interface for the Symbol model.

    Attributes:
        autocomplete_fields (list): Fields that should use an autocomplete widget.
        list_display (tuple): Fields to display in the list view.
        list_display_links (tuple): Fields that should link to the detail view.
        list_filter (tuple): Fields to filter the list view.
        search_fields (tuple): Fields that should be searchable.
    """

    autocomplete_fields = ("brokers", "market")
    list_display = ("pk", "name", "code", "type", "market")
    list_display_links = list_display
    list_filter = ("type", "market")
    search_fields = ("name", "code")


@admin.register(SymbolType)
class SymbolTypeAdmin(admin.ModelAdmin):
    """
    Admin interface options for the SymbolType model

    Attributes:
        list_display (tuple): Fields to display in the list view of the admin interface.
        list_display_links (tuple): Fields that will link to the detail view in the admin interface.
        search_fields (tuple): Fields that can be searched using the search bar in the admin interface.
    """

    list_display = ("pk", "name")
    list_display_links = list_display
    search_fields = ("name",)
