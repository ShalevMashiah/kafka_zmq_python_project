from abc import ABC, abstractmethod
from typing import Callable


class IKafkaManager(ABC):
    @abstractmethod
    def send_message(self, topic: str, msg: str) -> None:
        pass
