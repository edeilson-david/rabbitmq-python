from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from application.fanout.exchange import FanoutExchange
from rabbitmq.queue import Queue


class FanoutConsumerSms(Consumer):

    def callback(self, channel, method, properties, body) -> None:
        print("SMS: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = FanoutExchange(name="fanout.notify")
        queue = Queue(name="fanout.sms")

        channel.bind_queue(queue=queue, exchange=exchange)
        channel.basic_consume(queue=queue, consumer=FanoutConsumerSms())
