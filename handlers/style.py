from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from dals.style_dal import StyleDAL
from schemas import Style

__all__ = (
    "get_user_style",
)


async def get_user_style(user_id: int, async_session: AsyncSession) -> Union[Style | None]:
    async with async_session.begin():
        style_dal = StyleDAL(async_session)
        return await style_dal.get_user_style(user_id=user_id)


async def get_style_by_name(style_name: str, async_session: AsyncSession) -> Union[Style | None]:
    async with async_session.begin():
        style_dal = StyleDAL(async_session)
        return await style_dal.get_style_by_style_name(style_name)
