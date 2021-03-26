from abc import abstractmethod, ABC
from typing import Optional

from core.entities import Message, TelegramUser, TelegramDialog


class IMessageProvider(ABC):
    @abstractmethod
    async def authorize_user(self, phone_number: str, password: str = None,
                             code: str = None) -> TelegramUser: ...

    @abstractmethod
    async def get_user_dialogs(self) -> list[TelegramDialog]: ...

    @abstractmethod
    async def get_dialog_messages(self, dialog_id: str, username: Optional[str],
                                  offset: str, limit: str) -> list[Message]: ...

    @abstractmethod
    async def send_message(self, receiver_id: str, message: str) -> Message: ...

    @abstractmethod
    async def logout(self) -> bool: ...
