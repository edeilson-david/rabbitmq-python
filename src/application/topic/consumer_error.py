from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer

from application.topic.exchange import TopicExchange
from rabbitmq.queue import Queue


class TopicConsumerError(Consumer):

    def callback(self, channel, method, properties, body) -> None:
        print("ERROR: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = TopicExchange(name="topic.log")
        queue = Queue(name="topic.error")

        channel.bind(queue=queue, exchange=exchange, routing_key="log.error")
        channel.basic_consume(queue=queue, consumer=TopicConsumerError())
