from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, BigInteger, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base, str_32, str_128, str_64, str_16
from .custom_columns import intpk, created_at

__all__ = (
    "User",
)


class User(Base):
    __tablename__ = 'users_user'

    id: Mapped[intpk]
    username: Mapped[str_32] = mapped_column(unique=True)
    password: Mapped[str_128]
    last_login: Mapped[datetime]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    first_name = mapped_column(String(150), nullable=False, default="Ivan")
    last_name = mapped_column(String(150), nullable=False, default="Ivanov")
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    date_joined: Mapped[created_at]
    chat_id: Mapped[Optional[str_64]]
    email = Column(String(254), nullable=True)
    date_of_payment: Mapped[Optional[datetime]]
    date_payment_expired: Mapped[Optional[datetime]]
    account_id: Mapped[Optional[int]]
    preset: Mapped[Optional[str_128]]
    remain_messages: Mapped[Optional[int]] = mapped_column(default=0)
    remain_paid_messages: Mapped[Optional[int]] = mapped_column(default=0)
    stable_account_id: Mapped[Optional[int]]
    is_test_user: Mapped[bool] = mapped_column(default=False)
    remain_video_messages: Mapped[Optional[int]] = mapped_column(default=0)
    used_test_video_payment: Mapped[bool] = mapped_column(default=False)
    video_preset: Mapped[Optional[str_16]]

    style_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users_style.id", ondelete='SET NULL'),
    )
    style: Mapped[Optional["Style"]] = relationship(
        back_populates='users',
        primaryjoin="Style.id == User.style_id"
    )

    custom_settings_id = Column(
        BigInteger,
        ForeignKey("users_customsettings.id", ondelete='SET NULL'),
        nullable=True,
    )
    custom_settings: Mapped[Optional["CustomSettings"]] = relationship(
        back_populates='users',
        primaryjoin="CustomSettings.id == User.custom_settings_id"
    )

    orders: Mapped[Optional[list["Order"]]] = relationship(
        back_populates="user",
        primaryjoin="User.id == Order.user_id"
    )
    stable_messages: Mapped[Optional[list["StableMessage"]]] = relationship(
        back_populates="user",
        primaryjoin="User.id == StableMessage.user_id"
    )

    def __repr__(self) -> str:
        return self.username

    @property
    def get_bot_end(self):
        try:
            return self.date_payment_expired.strftime("%d-%m-%Y %H:%M") or "Оплат пока не было(("
        except Exception:
            return "Оплат пока не было(("

    @property
    def all_messages(self):
        if self.date_payment_expired and self.date_payment_expired.replace(tzinfo=None) > datetime.now():
            return self.remain_messages + self.remain_paid_messages
        return self.remain_messages
