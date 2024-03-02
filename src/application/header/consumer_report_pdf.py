from application.header.exchange import HeaderExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.consumer import Consumer
from rabbitmq.queue import Queue


class HeaderConsumerReportPdf(Consumer):
    """
    This consumer will only consider messages that contain the header as format=pdf AND type=report.
    """

    def callback(self, channel, method, properties, body) -> None:
        print("Report PDF: [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    with ConnectionManager() as connection_manager:
        channel = Channel(connection_manager)

        exchange = HeaderExchange(name="header.notify")

        args = {
            "x-match": "all",
            "format": "pdf",
            "type": "report"
        }
        queue = Queue(name="header.report_pdf")

        channel.bind(queue=queue, exchange=exchange, routing_key="", headers=args)
        channel.basic_consume(queue=queue, consumer=HeaderConsumerReportPdf())
