from abc import ABC, abstractmethod


class Consumer(ABC):

    @abstractmethod
    def callback(self, ch, method, properties, body) -> None:
        pass
