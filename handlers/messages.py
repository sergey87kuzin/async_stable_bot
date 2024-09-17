from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dals import StableMessageDAL

__all__ = (
    "_update_message",
    "_create_message",
    "get_message_by_id",
    "get_message_by_stable_request_id",
    "get_not_sent_to_stable_messages",
    "get_no_answer_messages",
    "get_not_sent_to_telegram_messages"
)

from schemas import StableMessage


async def _update_message(message_id: int, update_data: dict, session: AsyncSession) -> Union[StableMessage | None]:
    # async with session.begin():
    message_dal = StableMessageDAL(session)
    updated_message = await message_dal.update_message(message_id, update_data)
    if not updated_message:
        return None
    await session.commit()
    return updated_message


async def _create_message(message_data: dict, session: AsyncSession) -> StableMessage:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        message = await message_dal.create_message(message_data)
        await session.commit()
        return message


async def get_message_by_id(message_id: int, session: AsyncSession) -> StableMessage:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        message = await message_dal.get_message_by_id(message_id)
        return message


async def get_message_by_stable_request_id(stable_request_id: str, session: AsyncSession) -> StableMessage:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        message = await message_dal.get_message_by_stable_request_id(stable_request_id)
        return message


async def get_not_sent_to_stable_messages(session: AsyncSession) -> list[StableMessage | None]:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        messages = await message_dal.get_not_sent_to_stable_messages()
        return messages


async def get_no_answer_messages(session: AsyncSession) -> list[StableMessage | None]:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        messages = await message_dal.get_no_answer_messages()
        return messages


async def get_not_sent_to_telegram_messages(session: AsyncSession) -> list[StableMessage | None]:
    async with session.begin():
        message_dal = StableMessageDAL(session)
        messages = await message_dal.get_not_sent_to_telegram_messages()
        return messages
