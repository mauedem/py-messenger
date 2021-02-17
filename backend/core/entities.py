from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
        username: str
        nickname: str
        password: str


@dataclass
class Message:
        sender: User
        reciever: User
        text: str
        created_at: datetime
