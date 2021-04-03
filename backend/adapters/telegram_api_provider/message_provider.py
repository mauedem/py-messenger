import asyncio
import os
from os.path import join
from typing import Optional

from telethon.sessions import StringSession
from telethon.tl.types import User, PeerUser, Channel

from boot import settings
from core.entities import Message, TelegramUser, TelegramDialog, TelegramChat, \
    TelegramChannel
from core.message_provider import IMessageProvider
# from telethon import TelegramClient
from telethon.sync import TelegramClient

from config import (API_ID, API_HASH)


class TelegramMessageProvider(IMessageProvider):
    # current_user = None
    # TODO убрать заглушку на свои креды
    current_user = TelegramUser(
        id=412300498,
        first_name='Eryn',
        last_name='Drem',
        username='eryndrem',
        phone='79530490707',
        avatar_id='',
    )

    @staticmethod
    def get_authorized_user_session():
        session_key = os.environ.get('SESSION_KEY')
        if not session_key:
            with open('session.txt', 'r') as txt_file:
                session_key = txt_file.read()

        return TelegramClient(StringSession(session_key), API_ID, API_HASH)

    async def authorize_user(self, phone_number: str, password: str = None,
                             code: str = None) -> TelegramUser:
        client = TelegramClient('user-session', API_ID, API_HASH)

        session_key = StringSession.save(client.session)
        os.environ['SESSION_KEY'] = session_key
        with open('session.txt', 'w') as txt_file:
            txt_file.write(session_key)

        await client.start(
            phone=lambda: phone_number,
            password=lambda: password,
            code_callback=lambda: code,
            max_attempts=1,
        )

        user = await client.get_me()

        file_id = 'user_avatar.jpg'
        avatar_path = join(settings.AVATARS_PATH, file_id)
        asyncio.create_task(self.download_avatar(client, avatar_path, user))

        self.current_user = TelegramUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            phone=user.phone,
            avatar_id=avatar_path,
        )

        return self.current_user

    @staticmethod
    async def download_avatar(client: TelegramClient, avatar_path: str, entity):
        with open(avatar_path, 'wb') as f:
            is_exist = await client.download_profile_photo(
                entity=entity,
                file=f,

            )
        if not is_exist:
            os.remove(avatar_path)

    async def get_user_dialogs(self) -> list[TelegramDialog]:
        client = self.get_authorized_user_session()
        await client.connect()

        dialogs = await client.get_dialogs()

        result = []
        tasks = []
        for dialog in dialogs:
            file_id = str(dialog.entity.id) + '.jpg'
            avatar_path = join(settings.AVATARS_PATH, file_id)

            tasks.append(self.download_avatar(client, avatar_path, dialog.entity))

            if isinstance(dialog.entity, User):
                entity = TelegramUser(
                    id=dialog.entity.id,
                    first_name=dialog.entity.first_name,
                    last_name=dialog.entity.last_name,
                    username=dialog.entity.username,
                    phone=dialog.entity.phone,
                    avatar_id=file_id,
                )
            elif isinstance(dialog.entity, Channel):
                admin_rights = False
                if dialog.entity.admin_rights:
                    admin_rights = dialog.entity.admin_rights.change_info

                entity = TelegramChannel(
                    id=dialog.entity.id,
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                    username=dialog.entity.username,
                    avatar_id=file_id,
                    admin_rights=admin_rights
                )
            else:
                entity = TelegramChat(
                    id=dialog.entity.id,
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                    avatar_id=file_id,
                )

            try:
                if isinstance(dialog.message.from_id, PeerUser):
                    sender_id = dialog.message.from_id.user_id
                else:
                    sender_id = dialog.message.from_id.channel_id
            except AttributeError:
                if isinstance(dialog.message.peer_id, PeerUser):
                    sender_id = dialog.message.peer_id.user_id
                else:
                    sender_id = dialog.message.peer_id.channel_id

            message = Message(
                id=dialog.message.id,
                sender_id=sender_id,
                text=dialog.message.message,
                created_at=dialog.message.date,
                media=None
            )

            result.append(TelegramDialog(
                name=dialog.name,
                entity=entity,
                message=message
            ))

        await asyncio.gather(*tasks)

        return result

    # TODO сделать загрузку, видео, стикеров и прочих документов
    @staticmethod
    async def download_message_media(client: TelegramClient, media_path: str,
                                     message):
        # TODO подумать насчет видео
        with open(media_path, 'wb') as f:
            is_exist = await client.download_media(
                message=message,
                file=f,
            )
        if not is_exist:
            os.remove(media_path)

    async def get_dialog_messages(self, dialog_id: str, username: Optional[str],
                                  offset: str, limit: str) -> list[Message]:
        client = self.get_authorized_user_session()
        await client.connect()

        try:
            entity = await client.get_input_entity(int(dialog_id))
        except ValueError:
            entity = await client.get_input_entity(username)

        messages = await client.get_messages(
            entity=entity,
            limit=int(limit),
            add_offset=int(offset)
        )

        result = []
        tasks = []
        for message in messages:
            file_id = None

            # TODO переделать загрузку с медия не только на фото
            if message.media:
                file_id = str(message.id) + '.jpg'
                media_path = join(settings.MEDIA_PATH, file_id)

                tasks.append(self.download_message_media(
                    client, media_path, message
                ))

            try:
                if isinstance(message.from_id, PeerUser):
                    sender_id = message.from_id.user_id
                else:
                    sender_id = message.from_id.channel_id
            except AttributeError:
                if isinstance(message.peer_id, PeerUser):
                    sender_id = message.peer_id.user_id
                else:
                    sender_id = message.peer_id.channel_id

            message = Message(
                id=message.id,
                sender_id=sender_id,
                text=message.message,
                created_at=message.date,
                media=file_id
            )

            result.append(message)

        if tasks:
            await asyncio.gather(*tasks)

        return result

    async def send_message(self, receiver_id: str, message: str) -> Message:
        client = self.get_authorized_user_session()
        await client.connect()

        entity = await client.get_input_entity(int(receiver_id))

        message = await client.send_message(
            entity=entity,
            message=message
        )

        return Message(
            id=message.id,
            sender_id=self.current_user.id,
            text=message.message,
            created_at=message.date,
            media=message.media
        )

    async def logout(self):
        client = self.get_authorized_user_session()
        await client.connect()

        is_logout_successful = await client.log_out()
        await client.disconnect()

        return is_logout_successful
