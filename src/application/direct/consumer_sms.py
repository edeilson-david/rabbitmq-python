from application.direct.exchange import DirectExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.queue import Queue


class DirectConsumerSms(Consumer):

    def callback(self, channel, method, properties, body) -> None:
        print("SMS: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = DirectExchange(name="direct.notify")
        queue = Queue(name="direct.sms")

        channel.bind(queue=queue, exchange=exchange)
        channel.basic_consume(queue=queue, consumer=DirectConsumerSms())
