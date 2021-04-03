import datetime
from typing import Any, Union, Optional

import pytz as pytz
from inject import attr

from adapters.telegram_api_provider.message_provider import \
    TelegramMessageProvider
from boot import settings
from core.entities import TelegramUser, TelegramChannel
from core.message_provider import IMessageProvider
from core.repos import IMessengerRepository
from core.tokenizer import generate_jwt_token, decode_jwt_token

from config import (TELEGRAM_TIMEZONE, LOCAL_TIMEZONE)


class Service:
    repo: IMessengerRepository = attr(IMessengerRepository)
    telegram_provider: IMessageProvider = attr(TelegramMessageProvider)

    # Auth methods
    def register(self, username: str, nickname: str, password: str) -> dict:
        try:
            user = self.repo.create_user(
                username=username,
                nickname=nickname,
                password=password
            )

            return dict(
                username=user.username,
                nickname=user.nickname,
                password=user.password,
                telegram_credentials=None
            )
        except BaseException as error:
            raise error

    def authorize(self, login: str, password: str) -> str:
        try:
            user = self.repo.authorize_user(
                login=login,
                password=password
            )

            return generate_jwt_token({
                'username': user.username
            })
        except BaseException as error:
            raise error

    def authenticate(self, token: str) -> dict:
        try:
            username_dict = decode_jwt_token(token)

            username = username_dict['username']
            user = self.repo.get_user_by_username(username)

            if user.telegram_credentials:
                return dict(
                    username=user.username,
                    nickname=user.nickname,
                    password=user.password,
                    telegram_credentials=dict(
                        id=user.telegram_credentials.id,
                        first_name=user.telegram_credentials.first_name,
                        last_name=user.telegram_credentials.last_name,
                        username=user.telegram_credentials.username,
                        phone=user.telegram_credentials.phone,
                        avatar_id=user.telegram_credentials.avatar_id
                    )
                )

            return dict(
                username=user.username,
                nickname=user.nickname,
                password=user.password,
                telegram_credentials=None
            )
        except BaseException as error:
            raise error

    # Telegram methods
    async def telegram_authorize_user(self, username: str, phone_number: str, password: str,
                                      code: str = None) -> dict:
        telegram_user = await self.telegram_provider.authorize_user(
            phone_number=phone_number,
            password=password,
            code=code
        )

        self.repo.set_telegram_credentials(username, telegram_user)

        return dict(
            id=telegram_user.id,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            username=telegram_user.username,
            phone=telegram_user.phone,
            avatar_id=telegram_user.avatar_id
        )

    async def get_user_dialogs(self) -> list[dict[str, Any]]:
        dialogs = await self.telegram_provider.get_user_dialogs()

        result = []
        for dialog in dialogs:
            message_created_at = dialog.message.created_at
            current_date_and_time = datetime.datetime.now()

            local_timezone = pytz.timezone(LOCAL_TIMEZONE)
            telegram_timezone = pytz.timezone(TELEGRAM_TIMEZONE)
            localized_message_timestamp = message_created_at.replace(
                tzinfo=telegram_timezone
            ).astimezone(local_timezone)

            current_date_delta = datetime.timedelta(
                days=current_date_and_time.day,
                hours=current_date_and_time.hour
            )
            localized_message_timestamp_delta = datetime.timedelta(
                days=localized_message_timestamp.day,
                hours=localized_message_timestamp.hour
            )
            difference = current_date_delta - localized_message_timestamp_delta

            if not difference.days and difference.seconds//3600 <= current_date_and_time.hour:
                formatted_date = localized_message_timestamp.strftime("%H:%M")
            else:
                formatted_date = localized_message_timestamp.strftime("%d.%m.%Y")

            message = dict(
                id=dialog.message.id,
                sender_id=dialog.message.sender_id,
                text=dialog.message.text,
                created_at=formatted_date
            )

            if isinstance(dialog.entity, TelegramUser):
                entity = dict(
                    id=dialog.entity.id,
                    type='user',
                    first_name=dialog.entity.first_name,
                    last_name=dialog.entity.last_name,
                    username=dialog.entity.username,
                    phone=dialog.entity.phone,
                    avatar_id=dialog.entity.avatar_id,
                )
            elif isinstance(dialog.entity, TelegramChannel):
                channel_id = str(-100) + str(dialog.entity.id)

                entity = dict(
                    id=channel_id,
                    type='channel',
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                    username=dialog.entity.username,
                    avatar_id=dialog.entity.avatar_id,
                    admin_rights=dialog.entity.admin_rights
                )
            else:
                chat_id = -dialog.entity.id

                entity = dict(
                    id=chat_id,
                    type='chat',
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                    avatar_id=dialog.entity.avatar_id,
                )

            result.append(dict(
                name=dialog.name,
                entity=entity,
                message=message
            ))

        return result

    def get_photo(self, file_id: str) -> Optional[bytes]:
        return settings.AVATARS_BASE_URL + file_id

    async def get_dialog_messages(self, dialog_id: str, username: Optional[str],
                                  offset: str = 0, limit: str = 30) -> \
            list[dict[str, Union[str, int]]]:
        # TODO подумать, каким образом выводить дату сообщения
        messages = await self.telegram_provider.get_dialog_messages(
            dialog_id,
            username,
            offset,
            limit
        )

        result = []
        for message in messages:
            message_created_at = message.created_at
            local_timezone = pytz.timezone(LOCAL_TIMEZONE)
            telegram_timezone = pytz.timezone(TELEGRAM_TIMEZONE)
            localized_message_timestamp = message_created_at.replace(
                tzinfo=telegram_timezone
            ).astimezone(local_timezone)

            formatted_date = localized_message_timestamp.strftime("%d.%m.%Y, ""%H:%M")

            result.append(dict(
                id=message.id,
                created_at=formatted_date,
                sender_id=message.sender_id,
                text=message.text,
                media=message.media
            ))

        return list(reversed(result))

    async def send_message(self, receiver_id: str, message: str) -> \
            dict[str, Union[str, int]]:
        message = await self.telegram_provider.send_message(
            receiver_id,
            message
        )

        message_created_at = message.created_at
        local_timezone = pytz.timezone(LOCAL_TIMEZONE)
        telegram_timezone = pytz.timezone(TELEGRAM_TIMEZONE)
        localized_message_timestamp = message_created_at.replace(
            tzinfo=telegram_timezone
        ).astimezone(local_timezone)

        formatted_date = localized_message_timestamp.strftime(
            "%d.%m.%Y, ""%H:%M"
        )

        return dict(
            id=message.id,
            created_at=formatted_date,
            sender_id=message.sender_id,
            text=message.text,
            media=message.media
        )

    async def telegram_logout(self, username: str):
        self.repo.unset_telegram_credentials(username)

        return await self.telegram_provider.logout()
