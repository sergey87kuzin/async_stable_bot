from typing import Union

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ['StyleDAL']

from schemas import Style, User


class StyleDAL:
    """Data Access Layer for Style"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_styles(self) -> list[Style]:
        query = select(Style)
        async with self.db_session.begin():
            result = await self.db_session.execute(query)
            return list(result.scalars().all())

    async def get_user_style(self, user_id: int) -> Union[Style | None]:
        query = (
            select(Style)
            .join(User)
            .filter(User.id == user_id)
        )
        result = await self.db_session.execute(query)
        style_row = result.fetchone()
        if style_row:
            return style_row[0]

    async def get_style_by_style_name(self, style_name: str) -> Union[Style | None]:
        query = (
            select(Style)
            .filter(Style.name == style_name)
        )
        result = await self.db_session.execute(query)
        style_row = result.fetchone()
        if style_row:
            return style_row[0]
