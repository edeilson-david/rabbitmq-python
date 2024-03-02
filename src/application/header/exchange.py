from pika.exchange_type import ExchangeType

from rabbitmq.exchange import Exchange


class HeaderExchange(Exchange):

    def __init__(self, name: str) -> None:
        super().__init__(name, ExchangeType.headers)
