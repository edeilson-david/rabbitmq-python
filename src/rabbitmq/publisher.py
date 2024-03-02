from abc import abstractmethod, ABC

from rabbitmq.channel import Channel
from rabbitmq.exchange import Exchange


class Publisher(ABC):
    """
    Publisher (or Producer) is the component or application responsible for creating and sending messages.
    The producer publishes messages to exchanges in RabbitMQ.
    """

    @abstractmethod
    def publish(self, exchange: Exchange, channel: Channel) -> None:
        pass
