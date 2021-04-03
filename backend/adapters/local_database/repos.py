from core.entities import User, TelegramUser
from core.repos import IMessengerRepository
from core.tokenizer import hash_password

db = dict()


class LocalMessengerRepository(IMessengerRepository):

    def create_user(self, username: str, nickname: str, password: str) -> User:
        existing_user = db.get(username)

        if existing_user:
            raise Exception('User with such username already exists')

        hashed_password = hash_password(password)

        user = db[username] = dict(
            username=username,
            nickname=nickname,
            password=hashed_password,
            telegram_credentials=None
        )

        return User(**user)

    def authorize_user(self, login: str, password: str) -> User:
        user = db.get(login)

        hashed_password = hash_password(password)

        if not user or user['password'] != hashed_password:
            raise Exception('Invalid credentials')

        return User(**user)

    def get_user_by_username(self, username: str) -> User:
        user = db.get(username)

        if not user or user['username'] != username:
            raise Exception('Invalid token')

        if not user['telegram_credentials']:
            return User(**user)

        return User(
            username=user['username'],
            nickname=user['nickname'],
            password=user['password'],
            telegram_credentials=TelegramUser(
                id=user['telegram_credentials']['id'],
                first_name=user['telegram_credentials']['first_name'],
                last_name=user['telegram_credentials']['last_name'],
                username=user['telegram_credentials']['username'],
                phone=user['telegram_credentials']['phone'],
                avatar_id=user['telegram_credentials']['avatar_id']
            )
        )

    def set_telegram_credentials(self, username: str,
                                 telegram_user: TelegramUser):
        db[username]['telegram_credentials'] = dict(
            id=telegram_user.id,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            username=telegram_user.username,
            phone=telegram_user.phone,
            avatar_id=telegram_user.avatar_id
        )

    def unset_telegram_credentials(self, username: str):
        db[username]['telegram_credentials'] = None
