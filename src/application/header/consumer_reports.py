from application.header.exchange import HeaderExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.queue import Queue


class HeaderConsumerReports(Consumer):
    """
    This consumer will only consider messages that contain the header as type=report OR departament=medical.
    """

    def callback(self, channel, method, properties, body) -> None:
        print("Reports: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = HeaderExchange(name="header.notify")
        args = {
            "x-match": "any",
            "type": "report",
            "departament": "medical"
        }
        queue = Queue(name="header.report")

        channel.bind(queue=queue, exchange=exchange, routing_key="", headers=args)
        channel.basic_consume(queue=queue, consumer=HeaderConsumerReports())
