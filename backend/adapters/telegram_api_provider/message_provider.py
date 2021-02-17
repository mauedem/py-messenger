from core.entities import Message
from core.message_provider import IMessageProvider


class TelegramMessageProvider(IMessageProvider):

        def send_message(self, message: Message):
                pass
