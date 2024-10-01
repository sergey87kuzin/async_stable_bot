from typing import Union

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import UserCreate
from schemas import User

__all__ = (
    "UserDAL",
)


class UserDAL:
    """Data Access Layer for Users"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user_data: UserCreate) -> User:
        new_user = User(
            username=user_data.username,
            chat_id=str(user_data.telegram_chat_id),
            password=user_data.password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_user

    async def get_user_by_username(self, username: str) -> Union[User, None]:
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row:
            return user_row[0]

    async def get_user_with_style_and_custom_settings(self, username) -> Union[User, None]:
        query = (
            select(User)
            .where(User.username == username)
            .options(joinedload(User.style))
            .options(joinedload(User.custom_settings))
        )
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row:
            return user_row[0]

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.id)
        )
        result = await self.db_session.execute(query)
        deleted_user_id_row = result.fetchone()
        if deleted_user_id_row:
            await self.db_session.commit()
            return deleted_user_id_row[0]

    async def update_user(self, user_id: int, update_data: dict) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(update_data)
            .returning(User.id)
        )
        result = await self.db_session.execute(query)
        updated_user_id_row = result.fetchone()
        if updated_user_id_row:
            await self.db_session.commit()
            return updated_user_id_row[0]

    async def get_all_active_users(self) -> Union[list[User], None]:
        query = (
            select(User)
            .where(User.is_active == True)
        )
        result = await self.db_session.execute(query)
        user_rows = result.scalars()
        return list(user_rows)
