from typing import Any, Union

from inject import attr

from adapters.telegram_api_provider.message_provider import \
    TelegramMessageProvider
from core.entities import TelegramUser, TelegramChannel
from core.message_provider import IMessageProvider
from core.repos import IMessengerRepository
from core.tokenizer import generate_jwt_token, decode_jwt_token


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
                password=user.password
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

            return dict(
                username=user.username,
                nickname=user.nickname,
                password=user.password
            )
        except BaseException as error:
            raise error

    # Telegram methods
    async def telegram_authorize_user(self, phone_number: str, password: str,
                                      code: str = None) -> dict:
        try:
            telegram_user = await self.telegram_provider.authorize_user(
                phone_number=phone_number,
                password=password,
                code=code
            )

            return dict(
                id=telegram_user.id,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                username=telegram_user.username,
                phone=telegram_user.phone
            )
        except BaseException as error:
            print(str(error))
            raise error

    async def get_user_dialogs(self) -> list[dict[str, Any]]:
        dialogs = await self.telegram_provider.get_user_dialogs()

        result = []
        for dialog in dialogs:
            formatted_date = dialog.message.created_at \
                .strftime("%d/%m/%Y, ""%H:%M:%S")

            message = dict(
                id=dialog.message.id,
                sender_id=dialog.message.sender_id,
                text=dialog.message.text,
                created_at=formatted_date
            )

            if isinstance(dialog.entity, TelegramUser):
                entity = dict(
                    id=dialog.entity.id,
                    first_name=dialog.entity.first_name,
                    last_name=dialog.entity.last_name,
                    username=dialog.entity.username,
                    phone=dialog.entity.phone
                )
            elif isinstance(dialog.entity, TelegramChannel):
                channel_id = str(-100) + str(dialog.entity.id)

                entity = dict(
                    id=channel_id,
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                    username=dialog.entity.username
                )
            else:
                chat_id = -dialog.entity.id

                entity = dict(
                    id=chat_id,
                    title=dialog.entity.title,
                    creator=dialog.entity.creator,
                )

            result.append(dict(
                name=dialog.name,
                entity=entity,
                message=message
            ))

        return result

    async def get_dialog_messages(self, dialog_id: str, offset: str = 0,
                                  limit: str = 30) -> \
            list[dict[str, Union[str, int]]]:
        messages = await self.telegram_provider.get_dialog_messages(
            dialog_id,
            offset,
            limit
        )

        result = []
        for message in messages:
            formatted_date = message.created_at.strftime("%d/%m/%Y, ""%H:%M:%S")

            result.append(dict(
                id=message.id,
                created_at=formatted_date,
                sender_id=message.sender_id,
                text=message.text,
            ))

        return list(reversed(result))

    async def send_message(self, receiver_id: str, message: str) -> \
            dict[str, Union[str, int]]:
        message = await self.telegram_provider.send_message(
            receiver_id,
            message
        )

        formatted_date = message.created_at.strftime("%d/%m/%Y, ""%H:%M:%S")

        return dict(
            id=message.id,
            created_at=formatted_date,
            sender_id=message.sender_id,
            text=message.text,
        )
