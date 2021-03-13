from abc import abstractmethod, ABC

from core.entities import Message, TelegramUser, TelegramDialog


class IMessageProvider(ABC):
    @abstractmethod
    def authorize_user(self, phone_number: str, password: str = None,
                       code: str = None) -> TelegramUser: ...

    @abstractmethod
    def get_user_dialogs(self) -> list[TelegramDialog]: ...

    @abstractmethod
    def get_dialog_messages(self, dialog_type: str, dialog_id: str) -> \
        list[Message]: ...

    @abstractmethod
    def send_message(self, message: Message): ...
