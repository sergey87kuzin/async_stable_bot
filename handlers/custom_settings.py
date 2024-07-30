from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from dals.custom_settings import CustomSettingsDAL
from schemas import CustomSettings

__all__ = (
    "get_user_custom_settings",
)


async def get_user_custom_settings(user_id: int, async_session: AsyncSession) -> Union[CustomSettings | None]:
    async with async_session.begin():
        custom_settings_dal = CustomSettingsDAL(async_session)
        return await custom_settings_dal.get_user_custom_settings(user_id=user_id)
