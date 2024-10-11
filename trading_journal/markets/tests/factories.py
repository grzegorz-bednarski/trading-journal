import factory

from trading_journal.markets.models import Broker, Market, Symbol, SymbolType


class MarketFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Market instances.

    Attributes:
        name (str): The name of the market, generated using Faker.
    """

    class Meta:
        model = Market
        django_get_or_create = ("name",)

    name = factory.Faker("company")


class BrokerFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Broker instances.

    Attributes:
        name (str): The name of the broker, generated using Faker.

    Methods:
        markets(create, extracted, **kwargs): Adds markets to the broker if provided.
    """

    class Meta:
        model = Broker
        django_get_or_create = ("name",)

    name = factory.Faker("company")

    @factory.post_generation
    def markets(self, create, extracted, **kwargs):
        """
        Adds markets to the broker after creation.

        Args:
            create (bool): Whether the instance has been created.
            extracted (list[Market], optional): A list of markets to associate with the broker.
        """
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of markets were passed in, use them
            for market in extracted:
                self.markets.add(market)


class SymbolTypeFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating SymbolType instances.

    Attributes:
        name (str): The name of the symbol type, generated using Faker.
    """

    class Meta:
        model = SymbolType
        django_get_or_create = ("name",)

    name = factory.Faker("word")


class SymbolFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Symbol instances.

    Attributes:
        name (str): The name of the financial symbol, generated using Faker.
        code (str): The code of the financial symbol, generated using Faker.
        type (SymbolType): The type of the financial symbol, created using SymbolTypeFactory.
        market (Market): The market in which the financial symbol is traded, created using MarketFactory.

    Methods:
        brokers(create, extracted, **kwargs): Adds brokers to the symbol if provided.
    """

    class Meta:
        model = Symbol
        django_get_or_create = ("code", "market")

    name = factory.Faker("company")
    code = factory.Faker("bothify", text="???-####")
    type = factory.SubFactory(SymbolTypeFactory)
    market = factory.SubFactory(MarketFactory)

    @factory.post_generation
    def brokers(self, create, extracted, **kwargs):
        """
        Adds brokers to the symbol after creation.

        Args:
            create (bool): Whether the instance has been created.
            extracted (list[Broker], optional): A list of brokers to associate with the symbol.
        """
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of brokers were passed in, use them
            for broker in extracted:
                self.brokers.add(broker)
