from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class User:
    username: str
    nickname: str
    password: str


@dataclass
class Message:
    id: int
    sender_id: int
    text: str
    created_at: datetime


@dataclass
class TelegramUser:
    # TODO добавить аву юзера
    id: int
    first_name: str
    last_name: str
    username: str
    phone: str


@dataclass
class TelegramChat:
    # TODO добавить аву чата
    id: int
    title: str
    creator: bool


@dataclass
class TelegramChannel:
    # TODO добавить аву канала
    id: int
    title: str
    creator: bool
    username: str


@dataclass
class TelegramDialog:
    name: str
    entity: Union[TelegramUser, TelegramChat, TelegramChannel]
    message: Message
