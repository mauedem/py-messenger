from inject import attr

from core.repos import IMessengerRepository


class Service:
    repo: IMessengerRepository = attr(IMessengerRepository)

    def register(self, username: str, nickname: str, password: str) -> dict:
        try:
            user = self.repo.create_user(username, nickname, password)

            return dict(
                username=user.username,
                nickname=user.nickname,
                password=user.password,
            )
        except BaseException as error:
            raise error

    def authorize(self, login: str, password: str) -> str:
        ...

    def authenticate(self, token: str) -> dict:
        ...
