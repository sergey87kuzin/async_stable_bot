from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, str_128, str_2048
from .custom_columns import intpk

__all__ = (
    "Style",
)


class Style(Base):
    __tablename__ = "users_style"

    id: Mapped[intpk]
    name_for_menu: Mapped[str_128] = mapped_column(default="Стиль")
    name: Mapped[str_128]
    positive_prompt: Mapped[str_2048]
    negative_prompt: Mapped[Optional[str_2048]]

    users: Mapped[Optional[list["User"]]] = relationship(
        back_populates="style",
        primaryjoin="Style.id == User.style_id"
    )
