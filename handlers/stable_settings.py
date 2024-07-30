from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import StableSettings

__all__ = (
    "get_stable_settings",
)


async def get_stable_settings(async_session: AsyncSession) -> StableSettings:
    async with async_session.begin():
        result = await async_session.execute(select(StableSettings))
        return result.fetchone()[0]
