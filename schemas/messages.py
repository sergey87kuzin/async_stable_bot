from typing import Optional

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from global_constants import StableMessageTypeChoices
from . import str_2048, str_128, str_512, str_1024, Base, str_8, str_16
from schemas.custom_columns import intpk, created_at

__all__ = (
    "StableMessage",
)


class StableMessage(Base):
    __tablename__ = 'stable_messages_stablemessage'

    id: Mapped[intpk]
    initial_text: Mapped[str_2048]
    eng_text: Mapped[str_2048]
    telegram_chat_id: Mapped[str_128]
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users_user.id", ondelete='CASCADE'),
    )
    user: Mapped["User"] = relationship(
        back_populates='stable_messages',
        primaryjoin="User.id == StableMessage.user_id"
    )
    stable_request_id: Mapped[Optional[str_512]]
    single_image: Mapped[Optional[str_1024]]
    first_image: Mapped[Optional[str_1024]]
    second_image: Mapped[Optional[str_1024]]
    third_image: Mapped[Optional[str_1024]]
    fourth_image: Mapped[Optional[str_1024]]
    answer_sent = Column(Boolean, default=False)
    sent_to_stable = Column(Boolean, default=True)
    width: Mapped[Optional[str_8]]
    height: Mapped[Optional[str_8]]
    seed: Mapped[Optional[str_16]]
    created_at: Mapped[created_at]
    message_type = Column(
        String(128),
        default=StableMessageTypeChoices.FIRST
    )
    new_endpoint = Column(Boolean, default=False)
