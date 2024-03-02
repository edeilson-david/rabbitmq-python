from application.direct.exchange import DirectExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.queue import Queue


class DirectConsumerAppchat(Consumer):
    """
    This consumer is responsible for reading the message from direct.appchat_dl queue.
    The messages within the queue has TTL (time-to-live) defined as 5 seconds.
    If the TTL is exceeded, the message is redirect to exchange direct.notify_dlx (considering the routing_key configured).
    """

    def callback(self, channel, method, properties, body) -> None:
        print("AppChat: disable for testing")
        channel.basic_nack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = DirectExchange(name="direct.notify_dl")
        queue_args = {"x-message-ttl": 5000, "x-dead-letter-exchange": "direct.notify_dlx", "x-dead-letter-routing-key": "appchat_dlq"}
        queue = Queue(name="direct.appchat_dl", args=queue_args)

        channel.bind(queue=queue, exchange=exchange, routing_key="appchat")
        channel.basic_consume(queue=queue, consumer=DirectConsumerAppchat())
