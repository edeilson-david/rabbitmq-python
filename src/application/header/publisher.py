import json
from pika.delivery_mode import DeliveryMode
from pika.spec import BasicProperties

from application.header.exchange import HeaderExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.exchange import Exchange
from rabbitmq.publisher import Publisher


class HeaderPublisher(Publisher):
    """
    Publishes notifications to a Header Exchange.
    """

    def __init__(self) -> None:
        self.notifications = [
            {
                "format": "pdf",
                "type": "report",
                "content": "file.pdf",
                "departament": "financial"
            },
            {
                "format": "txt",
                "type": "log",
                "content": "INFO: msg='This is a message.'",
                "departament": "it"
            },
            {
                "format": "zip",
                "type": "report",
                "content": "report1.zip, report2.zip",
                "departament": "management"
            },
            {
                "format": "zip",
                "type": "exams",
                "content": "report1.zip, report2",
                "departament": "medical"
            }

        ]

    def publish(self, exchange: Exchange, channel: Channel) -> None:
        for notification in self.notifications:
            properties = BasicProperties(
                headers={"format": notification["format"], "type": notification["type"], "departament": notification["departament"]},
                content_type="domain/json",
                content_encoding="UTF-8",
                delivery_mode=DeliveryMode.Persistent)

            channel.basic_publish(
                exchange=exchange,
                routing_key="",
                message=json.dumps(notification),
                properties=properties)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        publisher = HeaderPublisher()
        publisher.publish(exchange=HeaderExchange(name="header.notify"), channel=Channel(connection_manager))
