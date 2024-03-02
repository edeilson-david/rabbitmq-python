import json
from pika.delivery_mode import DeliveryMode
from pika.spec import BasicProperties

from application.fanout.exchange import FanoutExchange
from rabbitmq.channel import Channel
from rabbitmq.connection import ConnectionManager
from rabbitmq.exchange import Exchange
from rabbitmq.publisher import Publisher


class FanoutPublisher(Publisher):
    """
    Publishes notifications to a Fanout Exchange.
    """

    def __init__(self) -> None:
        self.notifications = [
            {
                "type": "sms",
                "recipient": "+551234567890",
                "message": "Olá! Sua entrega está a caminho. Acompanhe o status pelo link: [www.rabbitmqstore.com]",
                "sender": "RabbitMQ Store",
                "date": "2024-02-29T12:30:00"
            },
            {
                "type": "appchat",
                "recipient": "+551234567890",
                "message": {
                    "text": "Oi! Tudo bem?",
                    "answer_options": ["Sim", "Não"]
                },
                "sender": "Vendedor",
                "date": "2024-02-29T13:45:00"
            },
            {
                "type": "email",
                "to": "dev.mq@rabbitmqstore.com",
                "subject": "Confirmação de Cadastro",
                "body": "Olá! Obrigado por se cadastrar conosco. Sua conta foi criada com sucesso.",
                "from": "contato@rabbitmqstore.com",
                "date": "2024-02-29T15:00:00"
            }
        ]

    def publish(self, exchange: Exchange, channel: Channel) -> None:
        properties = BasicProperties(content_type="domain/json", content_encoding="UTF-8", delivery_mode=DeliveryMode.Persistent)
        for notification in self.notifications:
            channel.basic_publish(
                exchange=exchange,
                routing_key="",
                message=json.dumps(notification),
                properties=properties)


if __name__ == "__main__":

    with ConnectionManager() as connection_manager:
        publisher = FanoutPublisher()
        publisher.publish(exchange=FanoutExchange(name="fanout.notify"), channel=Channel(connection_manager))
