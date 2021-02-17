from abc import ABC, abstractmethod

from core.entities import User


class IMessengerRepository(ABC):
    @abstractmethod
    def create_user(self, username: str, nickname: str, password: str) -> User:
        ...

    @abstractmethod
    def authorize_user(self, username: str, password: str) -> User: ...

    @abstractmethod
    def get_user_by_username(self, username: str) -> User: ...

    @abstractmethod
    def delete_user(self, username: str) -> None: ...
