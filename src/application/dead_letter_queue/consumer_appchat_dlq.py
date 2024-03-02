from application.direct.exchange import DirectExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.queue import Queue


class DirectConsumerAppchatDlq(Consumer):
    """
    This consumer is responsible for reading redirected messages because the TTL (time-to-live) has been exceeded.
    In this case, a specific treatment for the messages can be applied, such as: redirect to the original queue or anything rule.
    """

    def callback(self, channel, method, properties, body) -> None:
        print("AppChatDlq: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = DirectExchange(name="direct.notify_dlx")
        queue = Queue(name="direct.appchat_dlq")

        channel.bind(queue=queue, exchange=exchange, routing_key="appchat_dlq")
        channel.basic_consume(queue=queue, consumer=DirectConsumerAppchatDlq())
