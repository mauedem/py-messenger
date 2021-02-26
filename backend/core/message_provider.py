from abc import abstractmethod, ABC

from core.entities import Message, TelegramUser


class IMessageProvider(ABC):
    @abstractmethod
    def authorize_user(self, phone_number: str, password: str = None,
                       code: str = None) -> TelegramUser:
        ...

    @abstractmethod
    def send_message(self, message: Message): ...
