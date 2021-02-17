from core.entities import User
from core.repos import IMessengerRepository
from core.utils import hash_password

db = dict()


class PsqlMessengerRepository(IMessengerRepository):

    def create_user(self, username: str, nickname: str, password: str) -> User:
        existing_user = db.get(username)

        if existing_user:
            raise Exception('User with such username already exists')

        hashed_password = hash_password(password)

        db[username] = dict(
            username=username,
            nickname=nickname,
            password=hashed_password
        )

        user = db[username]

        return User(
            username=user['username'],
            nickname=user['nickname'],
            password=user['password']
        )

    def authorize_user(self, username: str, password: str) -> User:
        pass

    def get_user_by_username(self, username: str) -> User:
        pass

    def delete_user(self, username: str) -> None:
        pass
