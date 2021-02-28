from telethon.tl.types import User, Chat, PeerUser, PeerChannel

from core.entities import Message, TelegramUser, TelegramDialog, TelegramChat, \
    TelegramChannel
from core.message_provider import IMessageProvider
from telethon import TelegramClient
from telethon.sync import TelegramClient

api_id = 3487673
api_hash = '214be9c66044d5e5fb88783977990384'


class TelegramMessageProvider(IMessageProvider):
    async def authorize_user(self, phone_number: str, password: str = None,
                             code: str = None) -> TelegramUser:
        client = TelegramClient('user_session', api_id, api_hash)

        await client.start(
            code_callback=lambda: code,
            phone=lambda: phone_number,
            password=lambda: password,
        )

        user = await client.get_me()

        return TelegramUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            phone=user.phone,
        )

    def get_user_dialogs(self) -> list[TelegramDialog]:
        with TelegramClient('user_session', api_id, api_hash) as client:
            dialogs = client.get_dialogs()

            result = []
            for dialog in dialogs:
                if isinstance(dialog.entity, User):
                    entity = TelegramUser(
                        id=dialog.entity.id,
                        first_name=dialog.entity.first_name,
                        last_name=dialog.entity.last_name,
                        username=dialog.entity.username,
                        phone=dialog.entity.phone
                    )
                elif isinstance(dialog.entity, Chat):
                    entity = TelegramChat(
                        id=dialog.entity.id,
                        title=dialog.entity.title,
                        creator=dialog.entity.creator
                    )
                else:
                    entity = TelegramChannel(
                        id=dialog.entity.id,
                        title=dialog.entity.title,
                        creator=dialog.entity.creator
                    )

                try:
                    if isinstance(dialog.message.from_id, PeerUser):
                        sender_id = dialog.message.from_id.user_id
                    else:
                        sender_id = dialog.message.from_id.channel_id
                except AttributeError:
                    sender_id = dialog.message.from_id

                message = Message(
                    sender_id=sender_id,
                    text=dialog.message.message,
                    created_at=dialog.message.date
                )

                result.append(TelegramDialog(
                    name=dialog.name,
                    entity=entity,
                    message=message
                ))

            return result

    def send_message(self, message: Message):
        pass
