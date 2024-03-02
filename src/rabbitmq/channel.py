from __future__ import annotations

from typing import Optional

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties

from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.exchange import Exchange
from rabbitmq.queue import Queue


class Channel(object):
    """
    A channel is a communication pathway or virtual connection within a connection.
    Channels are a fundamental concept in the AMQP (Advanced Message Queuing Protocol) model, which RabbitMQ adheres
    to. They provide a way for multiple, independent streams of communication to exist within a single connection.

    When working with RabbitMQ in programming, applications interact with the broker through channels.
    Channels are created within a connection, and different operations, such as publishing, consuming,
    or declaring queues and exchanges, are performed within specific channels.

    It's important to note that channels are specific to the AMQP protocol and are not unique to RabbitMQ;
    they are a general concept in AMQP-based messaging systems. The use of channels enhances the flexibility and
    efficiency of communication in RabbitMQ.
    """

    def __init__(self, connection_manager: ConnectionManager) -> None:
        self._connection_manager = connection_manager
        self._channel: Optional[BlockingChannel] = self._connection_manager.get_channel()

    def exchange_declare(self, exchange: Exchange) -> None:
        self._validated_channel()
        self._channel.exchange_declare(exchange=exchange.name, exchange_type=exchange.type, durable=True)

    def queue_declare(self, queue: Queue) -> None:
        self._validated_channel()
        self._channel.queue_declare(queue=queue.name, durable=True)

    def bind(self, queue: Queue, exchange: Exchange, routing_key: str = None, headers: dict = None) -> None:
        self.exchange_declare(exchange=exchange)
        self.queue_declare(queue=queue)
        self.bind_queue(queue=queue, exchange=exchange, routing_key=routing_key, headers=headers)

    def bind_queue(self, queue: Queue, exchange: Exchange, routing_key: str = None, headers: dict = None) -> None:
        self._validated_channel()
        self._channel.queue_bind(queue=queue.name, exchange=exchange.name, routing_key=routing_key, arguments=headers)

    def bind_exchange(self, destination: Exchange, source: Exchange, routing_key: str = "") -> None:
        self._validated_channel()
        self._channel.exchange_bind(destination=destination, source=source, routing_key=routing_key)

    def is_open(self) -> bool:
        return self._channel is not None and self._channel.is_open

    def is_closed(self) -> bool:
        return self._channel is not None and self._channel.is_closed

    def basic_publish(self, exchange: Exchange, routing_key: str, message: Optional[str | bytes], properties: BasicProperties) -> None:
        self._validated_channel()
        self._channel.basic_publish(exchange=exchange.name, routing_key=routing_key, body=message, properties=properties)

    def basic_consume(self, consumer: Consumer, queue: Queue) -> None:
        self._validated_channel()
        self._channel.basic_consume(queue=queue.name, on_message_callback=consumer.callback)

        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.start_consuming()

    def _validated_channel(self) -> None:
        if self.is_closed():
            self._channel = self._connection_manager.get_channel()
