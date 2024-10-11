from django.test import TestCase

from trading_journal.markets.models import Broker
from trading_journal.markets.models import Market
from trading_journal.markets.models import Symbol
from trading_journal.markets.models import SymbolType
from trading_journal.markets.tests.factories import BrokerFactory
from trading_journal.markets.tests.factories import MarketFactory
from trading_journal.markets.tests.factories import SymbolFactory
from trading_journal.markets.tests.factories import SymbolTypeFactory


class MarketTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up a Market instance for testing.
        """
        self.market = MarketFactory()

    def test_market_creation(self) -> None:
        """
        Test that a Market instance is created correctly.
        """
        self.assertIsInstance(self.market, Market)
        self.assertIsNotNone(self.market.name)

    def test_market_string_representation(self) -> None:
        """
        Test the string representation of the Market model.
        """
        self.assertEqual(str(self.market), self.market.name)


class BrokerTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up a Broker instance for testing.
        """
        self.broker = BrokerFactory()
        self.markets = MarketFactory.create_batch(3)
        self.broker.markets.set(self.markets)

    def test_broker_creation(self) -> None:
        """
        Test that a Broker instance is created correctly.
        """
        self.assertIsInstance(self.broker, Broker)
        self.assertIsNotNone(self.broker.name)

    def test_broker_string_representation(self) -> None:
        """
        Test the string representation of the Broker model.
        """
        self.assertEqual(str(self.broker), self.broker.name)

    def test_broker_markets(self) -> None:
        """
        Test that the Broker instance has the correct markets associated.
        """
        self.assertEqual(self.broker.markets.count(), 3)
        self.assertListEqual(list(self.broker.markets.all()), self.markets)


class SymbolTypeTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up a SymbolType instance for testing.
        """
        self.symbol_type = SymbolTypeFactory()

    def test_symbol_type_creation(self) -> None:
        """
        Test that a SymbolType instance is created correctly.
        """
        self.assertIsInstance(self.symbol_type, SymbolType)
        self.assertIsNotNone(self.symbol_type.name)

    def test_symbol_type_string_representation(self) -> None:
        """
        Test the string representation of the SymbolType model.
        """
        self.assertEqual(str(self.symbol_type), self.symbol_type.name)


class SymbolTestCase(TestCase):
    def setUp(self) -> None:
        """
        Set up a Symbol instance for testing.
        """
        self.symbol = SymbolFactory()
        self.brokers = BrokerFactory.create_batch(2)
        self.symbol.brokers.set(self.brokers)

    def test_symbol_creation(self) -> None:
        """
        Test that a Symbol instance is created correctly.
        """
        self.assertIsInstance(self.symbol, Symbol)
        self.assertIsNotNone(self.symbol.name)
        self.assertIsNotNone(self.symbol.code)
        self.assertIsNotNone(self.symbol.type)
        self.assertIsNotNone(self.symbol.market)

    def test_symbol_string_representation(self) -> None:
        """
        Test the string representation of the Symbol model.
        """
        self.assertEqual(str(self.symbol), self.symbol.name)

    def test_symbol_brokers(self) -> None:
        """
        Test that the Symbol instance has the correct brokers associated.
        """
        self.assertEqual(self.symbol.brokers.count(), 2)
        self.assertListEqual(list(self.symbol.brokers.all()), self.brokers)
