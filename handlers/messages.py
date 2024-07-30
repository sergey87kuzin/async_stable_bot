from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dals import StableMessageDAL

__all__ = (
    "_update_message",
    "_create_message"
)

from schemas import StableMessage


async def _update_message(message_id: int, update_data: dict, session: AsyncSession) -> None:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        updated_message = await message_dal.update_message(message_id, update_data)
        if not updated_message:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Не удалось изменить данные сообщения"
            )


async def _create_message(message_data: dict, session: AsyncSession) -> StableMessage:
    # async with session.begin():
    message_dal = StableMessageDAL(session)
    message = await message_dal.create_message(message_data)
    await session.commit()
    return message
