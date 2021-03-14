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
    id: int
    first_name: str
    last_name: str
    username: str
    phone: str
    avatar_id: str


@dataclass
class TelegramChat:
    id: int
    title: str
    creator: bool
    avatar_id: str


@dataclass
class TelegramChannel:
    id: int
    title: str
    creator: bool
    username: str
    avatar_id: str


@dataclass
class TelegramDialog:
    name: str
    entity: Union[TelegramUser, TelegramChat, TelegramChannel]
    message: Message
