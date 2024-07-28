from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from . import Base
from .custom_columns import intpk

__all__ = (
    "Prolongation",
)


class Prolongation(Base):
    __tablename__ = 'courses_prolongation'

    id: Mapped[intpk]
    cost: Mapped[int]
    duration: Mapped[int]
    course_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses_course.id", ondelete='SET NULL'),
    )
    course: Mapped["Course"] = relationship(
        back_populates='prolongations',
        primaryjoin="Course.id == Prolongation.course_id"
    )
