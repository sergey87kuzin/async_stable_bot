from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import contains_eager, joinedload, Load, sessionmaker, selectinload

import settings
from models.custom_settings import ShowCustomSettings
from schemas import User, Style, CustomSettings

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()


class Training:
    @classmethod
    async def update_user(cls, data: dict):
        async with async_session.begin():
            query = (
                update(User)
                .where(and_(User.id == data.get("user_id"), User.is_active == True))
                .values(style_id=3)
                .returning(User.id, User.custom_settings_id)
            )
            result = await async_session.execute(query)
            user_id, custom_settings_id = result.fetchone()
            style_query = (
                select(Style.name_for_menu)
                .select_from(User)
                .join(User.style)
                .where(User.id == user_id)
            )
            style_result = await async_session.execute(style_query)
            print(style_result.scalar())
            custom_settings_query = (
                select(User)
                .options(
                    joinedload(User.custom_settings, innerjoin=True)
                    .load_only(CustomSettings.name, CustomSettings.model_id)
                )
                .options(Load(User).load_only(User.username))
                .where(User.id == user_id)
            )
            custom_settings_result = await async_session.execute(custom_settings_query)
            user = custom_settings_result.fetchone()[0]
            print(user.custom_settings.name, user.custom_settings.model_id, user.username)
            subquery = (
                select(User.id)
                .filter(User.custom_settings_id == CustomSettings.id)
                .limit(2)
                .scalar_subquery()
                .correlate(CustomSettings)
            )
            limit_query = (
                select(CustomSettings)
                .where(CustomSettings.id == custom_settings_id)
                .outerjoin(User, User.id.in_(subquery))
                .options(
                    contains_eager(CustomSettings.users)
                    .load_only(User.username, User.email, User.is_active, User.custom_settings_id),
                )
                .options(
                    Load(CustomSettings).load_only(CustomSettings.name, CustomSettings.model_id)
                )
            )
            limit_result = await async_session.execute(limit_query)
            result_orm = limit_result.unique().scalars().all()
            result_dto = [ShowCustomSettings.model_validate(row, from_attributes=True) for row in result_orm]
            print(result_dto)
