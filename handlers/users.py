from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dals import UserDAL
from hashing import Hasher
from models import UserCreate, ShowUser, DeleteUser, GetUserForMessageHandler

__all__ = (
    "_create_new_user",
    "_delete_user",
    "_update_user",
    "_get_user_by_username"
)


async def _create_new_user(body: UserCreate, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(body)
        return ShowUser(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
        )


async def _get_user_by_username(username: str, session: AsyncSession) -> GetUserForMessageHandler | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_username(username=username)
        if not user:
            return None
        return GetUserForMessageHandler(
            id=user.id,
            username=user.username,
            remain_messages=user.remain_messages,
            remain_paid_messages=user.remain_paid_messages,
            date_payment_expired=user.date_payment_expired,
        )


async def _delete_user(user_id: int, session: AsyncSession) -> DeleteUser:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(user_id)
        if not deleted_user_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Не удалось удалить пользователя"
            )
        return DeleteUser(id=deleted_user_id)


async def _update_user(user_id: int, update_data: dict, session: AsyncSession) -> DeleteUser:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(user_id, update_data)
        if not updated_user_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Не удалось изменить данные пользователя"
            )
        return DeleteUser(id=updated_user_id)
