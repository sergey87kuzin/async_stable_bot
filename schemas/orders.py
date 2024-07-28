from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from . import Base
from .custom_columns import intpk, created_at

__all__ = (
    "Order",
)


class Order(Base):
    __tablename__ = 'orders_order'

    id: Mapped[intpk]
    total_cost: Mapped[int]
    payment_url: Mapped[Optional[str]]
    days: Mapped[Optional[int]]
    payment_status: Mapped[str] = mapped_column(String(15), default="Not paid")
    created_at: Mapped[created_at]
    payment_date: Mapped[Optional[datetime]]
    message_count: Mapped[Optional[int]]
    video_message_count: Mapped[Optional[int]]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users_user.id", ondelete='CASCADE'),
    )
    user: Mapped[Optional["User"]] = relationship(
        back_populates='orders',
        primaryjoin="User.id == Order.user_id"
    )
    course_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses_course.id", ondelete='SET NULL'),
    )
    course: Mapped[Optional["Course"]] = relationship(
        back_populates='orders',
        primaryjoin="Course.id == Order.course_id"
    )
    prolongation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses_prolongation.id", ondelete='SET NULL'),
    )
    prolongation: Mapped[Optional["Prolongation"]] = relationship(
        back_populates='orders',
        primaryjoin="Prolongation.id == Order.prolongation_id"
    )
