from __future__ import annotations

from pika.exchange_type import ExchangeType


class Exchange(object):

    def __init__(self, name: str, type: ExchangeType) -> None:
        self.name: str = name
        self.type: str = type.value
