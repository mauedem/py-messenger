from typing import Optional

from pydantic import BaseModel


# Auth models
class CreateUserModel(BaseModel):
    username: str
    nickname: str
    password: str


class AuthorizeUserModel(BaseModel):
    login: str
    password: str


# TG models
class TelegramAuthorizeUserModel(BaseModel):
    phone_number: str
    password: Optional[str] = None
    code: Optional[str] = None


class TelegramSendMessageModel(BaseModel):
    receiver_id: str
    message: str
