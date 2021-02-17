from inject import attr

from core.repos import IMessengerRepository
from core.utils import generate_jwt_token, decode_jwt_token


class Service:
        repo: IMessengerRepository = attr(IMessengerRepository)

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
