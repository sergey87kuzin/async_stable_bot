from typing import Union

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ['CustomSettingsDAL']

from schemas import CustomSettings, User


class CustomSettingsDAL:
    """Data Access Layer for Style"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_custom_settings(self, user_id) -> Union[CustomSettings | None]:
        query = (
            select(CustomSettings)
            .join(User)
            .where(User.id == user_id)
        )
        # async with self.db_session.begin():
        result = await self.db_session.execute(query)
        if result:
            return result.fetchone()[0]
