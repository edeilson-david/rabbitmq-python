import json

from pika.delivery_mode import DeliveryMode
from pika.spec import BasicProperties

from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.exchange import Exchange
from rabbitmq.publisher import Publisher
from application.topic.exchange import TopicExchange


class TopicPublisher(Publisher):
    """
        Publishes notifications to a Topic Exchange.
        """

    def __init__(self) -> None:
        self.logs = [
            {
                "level": "debug",
                "timestamp": "2024-02-29T16:15:00",
                "message": "Debugging information for troubleshooting purposes.",
                "module": "app.moduleA",
                "details": {
                    "data": {"key": "value"},
                    "user_id": 12345
                }
            },
            {
                "level": "info",
                "timestamp": "2024-02-29T16:30:00",
                "message": "Application is running smoothly.",
                "module": "app.moduleB",
                "details": "n/a"
            },
            {
                "level": "warning",
                "timestamp": "2024-02-29T16:45:00",
                "message": "Warning: Resource usage is approaching limits.",
                "module": "app.moduleC",
                "details": {
                    "usage_percent": 80
                }
            },
            {
                "level": "error",
                "timestamp": "2024-02-29T17:00:00",
                "message": "Critical error occurred. Application will terminate.",
                "module": "app.moduleD",
                "details": {
                    "error_code": 500,
                    "error_message": "Internal Server Error"
                }
            }
        ]

    def publish(self, exchange: Exchange, channel: Channel) -> None:
        properties = BasicProperties(content_type="domain/json", content_encoding="UTF-8", delivery_mode=DeliveryMode.Persistent)
        for log in self.logs:
            channel.basic_publish(
                exchange=exchange,
                routing_key=f"log.{log['level']}",
                message=json.dumps(log),
                properties=properties)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        publisher = TopicPublisher()
        publisher.publish(exchange=TopicExchange(name="topic.log"), channel=Channel(connection_manager))
