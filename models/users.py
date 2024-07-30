from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from .common import TunedModel


__all__ = (
    "UserCreate",
    "ShowUser",
    "GetUserForMessageHandler",
    "DeleteUser"
)


class UserCreate(BaseModel):
    username: str
    password: str
    telegram_chat_id: int


class ShowUser(TunedModel):
    id: int
    username: str
    is_active: bool


class GetUserForMessageHandler(TunedModel):
    id: int
    username: str
    remain_messages: int
    remain_paid_messages: int
    date_payment_expired: Optional[datetime]
    preset: Optional[str]


class DeleteUser(TunedModel):
    id: int
