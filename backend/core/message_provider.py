from abc import abstractmethod, ABC

from core.entities import Message


class IMessageProvider(ABC):
    @abstractmethod
    def send_message(self, message: Message): ...
