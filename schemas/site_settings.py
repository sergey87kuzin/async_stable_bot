from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from schemas import Base, str_512, str_1024

__all__ = ['SiteSettings']

from schemas.custom_columns import intpk


class SiteSettings(Base):
    __tablename__ = 'bot_config_sitesettings'

    id: Mapped[intpk]
    day_tariff_cost: Mapped[int]
    month_tariff_cost: Mapped[int]
    say_hi_video: Mapped[Optional[str]]
    say_hi_video_video_bot: Mapped[Optional[str]]
    day_tariff_count: Mapped[int]
    month_tariff_count: Mapped[int]
    notice_message: Mapped[Optional[str_512]]
    settings_lesson_link: Mapped[Optional[str_1024]]
    # queue_number: Mapped[Optional[int]]
