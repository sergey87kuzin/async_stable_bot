from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.site_settings import SiteSettings


async def get_site_settings(async_session: AsyncSession) -> SiteSettings:
    result = await async_session.execute(select(SiteSettings))
    return result.fetchone()[0]
