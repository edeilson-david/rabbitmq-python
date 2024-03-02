from abc import ABC, abstractmethod


class Consumer(ABC):
    """
    Consumers are application or components that subscribe to a specific queue and retrieves messages from that queue for processing.
    Consumers play a crucial role in the asynchronous communication model facilitated by RabbitMQ, allowing for the decoupling of message producers and consumers.
    """

    @abstractmethod
    def callback(self, ch, method, properties, body) -> None:
        pass
