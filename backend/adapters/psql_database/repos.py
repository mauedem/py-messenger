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

    def authorize_user(self, login: str, password: str) -> User:
        user = db.get(login)

        hashed_password = hash_password(password)

        if not user or user['password'] != hashed_password:
            raise Exception('Invalid credentials')

        return User(
            username=user['username'],
            nickname=user['nickname'],
            password=user['password']
        )

    def get_user_by_username(self, username: str) -> User:
        user = db.get(username)

        if not user or user['username'] != username:
            raise Exception('Invalid token')

        return User(
            username=user['username'],
            nickname=user['nickname'],
            password=user['password']
        )
