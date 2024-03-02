from __future__ import annotations

from pika.exchange_type import ExchangeType


class Exchange(object):
    """
    An exchange is a routing mechanism that determines how messages should be distributed to queues.
    It plays a crucial role in the message routing process.

    When a producer sends a message to RabbitMQ, it doesn't send the message directly to a queue.
    Instead, it sends the message to an exchange.

    The exchange then routes the message to one or more queues based on specific rules or bindings.

    There are several types of exchanges in RabbitMQ, each with different routing logic:
    Direct Exchange: Routes messages with a specific routing key to a queue with the same key.
    Fanout Exchange: Broadcasts messages to all queues bound to it, regardless of the routing key.
    Topic Exchange: Allows more complex routing based on wildcard patterns in the routing key.
    Headers Exchange: Routes messages based on message header attributes, allowing for more fine-grained control over routing.
    Default Exchange (Direct Exchange with an empty name): Routes messages to queues with names matching the routing key.

    Exchanges provide flexibility in designing the message routing strategy within a RabbitMQ system.
    By using different exchange types and configuring bindings, you can implement various messaging patterns to suit the needs of your application.

    It is possible to bind an exchange to another exchange, and not only to queues.
    """

    def __init__(self, name: str, type: ExchangeType) -> None:
        self.name: str = name
        self.type: str = type.value
