from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ['StyleDAL']

from schemas import Style


class StyleDAL:
    """Data Access Layer for Users"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_styles(self) -> list[Style]:
        query = select(Style)
        async with self.db_session.begin():
            result = await self.db_session.execute(query)
            return list(result.scalars().all())
