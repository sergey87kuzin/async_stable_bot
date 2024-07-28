from typing import Optional

from sqlalchemy.orm import relationship, Mapped

from . import Base, str_256, str_512
from .custom_columns import intpk

__all__ = (
    "Course",
)


class Course(Base):
    __tablename__ = 'courses_course'

    id: Mapped[intpk]
    name: Mapped[str_256]
    cover: Mapped[str]
    cost: Mapped[int]
    duration: Mapped[int]
    is_active: Mapped[bool]
    description: Mapped[str_512]

    orders: Mapped[Optional[list["Order"]]] = relationship(
        back_populates="course",
        primaryjoin="Course.id == Order.course_id"
    )
    prolongations: Mapped[Optional[list["Prolongation"]]] = relationship(
        back_populates="course",
        primaryjoin="Course.id == Prolongation.course_id"
    )
