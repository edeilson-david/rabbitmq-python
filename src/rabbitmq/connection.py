from __future__ import annotations

from typing import Optional

from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from pika.connection import ConnectionParameters
from pika.exceptions import AMQPConnectionError


class ConnectionManager(object):
    """
    Manages connections to RabbitMQ. For teaching purposes is used the BlockingConnection strategy.
    """

    _instance = None

    def __new__(cls) -> None:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._connection: Optional[BlockingConnection] = None

    def __enter__(self) -> ConnectionManager:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> True:
        self.close()
        return True

    def connect(self) -> None:
        """
        Create a connection to the RabbitMQ using the default configurations.
        """
        if self.is_connected():
            return

        self._connection = BlockingConnection(ConnectionParameters())
        retries = 0
        while retries < 3:
            try:
                self._connection = BlockingConnection(ConnectionParameters())
                return
            except AMQPConnectionError:
                retries += 1

    def is_connected(self) -> bool:
        return self._connection is not None and self._connection.is_open

    def not_connected(self) -> bool:
        return self._connection is not None and self._connection.is_closed

    def close(self) -> None:
        if self.is_connected():
            self._connection.close()
            self._connection = None

    def get_channel(self) -> BlockingChannel:
        if self.not_connected():
            self.connect()

        return self._connection.channel()
