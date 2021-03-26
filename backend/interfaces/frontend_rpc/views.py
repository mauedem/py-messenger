from typing import Optional

from fastapi import Response, Cookie, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import RedirectResponse, JSONResponse

from core.services import Service
from interfaces.frontend_rpc.models import CreateUserModel, AuthorizeUserModel, \
    TelegramAuthorizeUserModel, TelegramSendMessageModel

router = InferringRouter()


@cbv(router)
class AppViews:
    service: Service = Depends(Service)

    @router.post('/private_api/auth/register/')
    def create_user_view(self, user: CreateUserModel):
        try:
            created_user = self.service.register(
                username=user.username,
                nickname=user.nickname,
                password=user.password
            )

            return created_user
        except BaseException as error:
            return str(error)

    @router.post('/private_api/auth/login/')
    def authorize_user_view(self, user: AuthorizeUserModel, response: Response):
        try:
            token = self.service.authorize(
                login=user.login,
                password=user.password
            )

            response.status_code = status.HTTP_200_OK
            response.set_cookie(key='token', value=token)

            return response
        except BaseException as error:
            return str(error)

    @router.get('/private_api/auth/authenticate/')
    def authenticate_user_view(self, token: str = Cookie(None)):
        user = self.service.authenticate(token)

        return user

    @router.post('/private_api/auth/logout/')
    def logout_user_view(self, response: Response):
        response.set_cookie(key='token', value='')
        response.status_code = status.HTTP_200_OK

        return response

    @router.post('/private_api/tg/authorize/')
    async def telegram_authorize_view(self, user: TelegramAuthorizeUserModel):
        try:
            user = await self.service.telegram_authorize_user(
                phone_number=user.phone_number,
                password=user.password,
                code=user.code
            )

            return user
        except BaseException as error:
            message = str(error)
            response = JSONResponse(content=message)
            response.status_code = 449

            return response

    @router.get('/private_api/tg/dialogs/')
    async def telegram_get_user_dialog_view(self):
        dialogs = await self.service.get_user_dialogs()

        return dialogs, 200

    @router.get('/private_api/tg/messages/')
    async def telegram_get_dialog_messages_view(
            self, dialog_id: str, username: Optional[str] = None,
            offset: Optional[str] = None, limit: Optional[str] = None
    ):
        data = dict(
            dialog_id=dialog_id,
            username=username,
            offset=offset,
            limit=limit
        )

        if not data['offset']:
            data.pop('offset')

        if not data['limit']:
            data.pop('limit')

        messages = await self.service.get_dialog_messages(**data)

        return messages

    @router.get('/private_api/tg/get_photo/')
    def telegram_get_photo_view(self, file_id: str):
        file = self.service.get_photo(file_id)
        file_path = f'http://localhost/{file}'

        return RedirectResponse(file_path)

    @router.post('/private_api/tg/send_message/')
    async def telegram_send_message_view(self,
                                         message: TelegramSendMessageModel):
        message = await self.service.send_message(
            receiver_id=message.receiver_id,
            message=message.message,
        )

        return message

    @router.post('/private_api/tg/logout/')
    async def telegram_logout_view(self):
        is_user_logout = await self.service.telegram_logout()

        if is_user_logout:
            message = 'User successfully logout'
            response = JSONResponse(content=message)
            response.status_code = 200

            return response

        message = 'User logout fail'
        response = JSONResponse(content=message)
        response.status_code = 418

        return response
