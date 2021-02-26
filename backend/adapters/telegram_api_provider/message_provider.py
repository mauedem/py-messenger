from telethon.errors import SessionPasswordNeededError
import asyncio

from core.entities import Message, TelegramUser
from core.message_provider import IMessageProvider
from telethon import TelegramClient

api_id = 3487673
api_hash = '214be9c66044d5e5fb88783977990384'


class TelegramMessageProvider(IMessageProvider):
    async def authorize_user(self, phone_number: str, password: str = None,
                             code: str = None) -> TelegramUser:
        client = TelegramClient('user_session', api_id, api_hash)

        await client.start(
            code_callback=lambda: code,
            phone=phone_number,
            password=password,
        )

        user = await client.get_me()

        return TelegramUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            phone=user.phone,
        )

    def send_message(self, message: Message):
        pass
