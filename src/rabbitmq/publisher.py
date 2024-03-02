from abc import abstractmethod, ABC

from rabbitmq.channel import Channel
from rabbitmq.exchange import Exchange


class Publisher(ABC):
    """
    Publisher abstract base class to publish messages to RabbitMQ Exchange.
    """

    @abstractmethod
    def publish(self, exchange: Exchange, channel: Channel) -> None:
        pass
