from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from trading_journal.markets.models import Broker, Market, Symbol, SymbolType
from trading_journal.users.tests.factories import UserFactory


class AdminSiteTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up instances for testing the admin interface.
        """
        self.user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.user)
        self.admin_site = admin.site

    def test_market_admin(self) -> None:
        """
        Test the Market model admin view.

        Ensures the Market changelist view is accessible.
        """
        url = reverse("admin:markets_market_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_broker_admin(self) -> None:
        """
        Test the Broker model admin view.

        Ensures the Broker changelist view is accessible.
        """
        url = reverse("admin:markets_broker_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_symbol_type_admin(self) -> None:
        """
        Test the SymbolType model admin view.

        Ensures the SymbolType changelist view is accessible.
        """
        url = reverse("admin:markets_symboltype_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_symbol_admin(self) -> None:
        """
        Test the Symbol model admin view.

        Ensures the Symbol changelist view is accessible.
        """
        url = reverse("admin:markets_symbol_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_broker_admin_autocomplete_fields(self) -> None:
        """
        Test that the autocomplete_fields for BrokerAdmin works as expected.

        Ensures that 'markets' is included in the autocomplete_fields of BrokerAdmin.
        """
        broker_admin = self.admin_site.get_model_admin(Broker)
        self.assertIn("markets", broker_admin.autocomplete_fields)

    def test_symbol_admin_autocomplete_fields(self) -> None:
        """
        Test that the autocomplete_fields for SymbolAdmin works as expected.

        Ensures that 'brokers' and 'market' are included in the autocomplete_fields of SymbolAdmin.
        """
        symbol_admin = self.admin_site.get_model_admin(Symbol)
        self.assertIn("brokers", symbol_admin.autocomplete_fields)
        self.assertIn("market", symbol_admin.autocomplete_fields)

    def test_list_display_fields_market(self) -> None:
        """
        Test that the list_display fields for MarketAdmin are correctly set.

        Ensures the list_display attribute of MarketAdmin matches the expected fields.
        """
        market_admin = self.admin_site.get_model_admin(Market)
        self.assertListEqual(list(market_admin.list_display), ["pk", "name"])

    def test_list_display_fields_broker(self) -> None:
        """
        Test that the list_display fields for BrokerAdmin are correctly set.

        Ensures the list_display attribute of BrokerAdmin matches the expected fields.
        """
        broker_admin = self.admin_site.get_model_admin(Broker)
        self.assertListEqual(
            list(broker_admin.list_display),
            ["pk", "name", "markets_names"],
        )

    def test_list_display_fields_symbol(self) -> None:
        """
        Test that the list_display fields for SymbolAdmin are correctly set.

        Ensures the list_display attribute of SymbolAdmin matches the expected fields.
        """
        symbol_admin = self.admin_site.get_model_admin(Symbol)
        self.assertListEqual(
            list(symbol_admin.list_display),
            ["pk", "name", "code", "type", "market"],
        )

    def test_list_filter_fields_symbol(self) -> None:
        """
        Test that the list_filter fields for SymbolAdmin are correctly set.

        Ensures the list_filter attribute of SymbolAdmin matches the expected fields.
        """
        symbol_admin = self.admin_site.get_model_admin(Symbol)
        self.assertListEqual(list(symbol_admin.list_filter), ["type", "market"])

    def test_search_fields_market(self) -> None:
        """
        Test that the search_fields for MarketAdmin are correctly set.

        Ensures the search_fields attribute of MarketAdmin matches the expected fields.
        """
        market_admin = self.admin_site.get_model_admin(Market)
        self.assertListEqual(list(market_admin.search_fields), ["name"])

    def test_search_fields_broker(self) -> None:
        """
        Test that the search_fields for BrokerAdmin are correctly set.

        Ensures the search_fields attribute of BrokerAdmin matches the expected fields.
        """
        broker_admin = self.admin_site.get_model_admin(Broker)
        self.assertListEqual(list(broker_admin.search_fields), ["name"])

    def test_search_fields_symbol(self) -> None:
        """
        Test that the search_fields for SymbolAdmin are correctly set.

        Ensures the search_fields attribute of SymbolAdmin matches the expected fields.
        """
        symbol_admin = self.admin_site.get_model_admin(Symbol)
        self.assertListEqual(list(symbol_admin.search_fields), ["name", "code"])

    def test_search_fields_symbol_type(self) -> None:
        """
        Test that the search_fields for SymbolTypeAdmin are correctly set.

        Ensures the search_fields attribute of SymbolTypeAdmin matches the expected fields.
        """
        symbol_type_admin = self.admin_site.get_model_admin(SymbolType)
        self.assertListEqual(list(symbol_type_admin.search_fields), ["name"])
