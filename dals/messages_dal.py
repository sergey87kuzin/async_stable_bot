from datetime import timedelta, datetime
from typing import Union

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from global_constants import StableMessageTypeChoices
from schemas import StableMessage, User

__all__ = (
    "StableMessageDAL",
)


class StableMessageDAL:
    """Data Access Layer for Users"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_message(self, message_data: dict) -> StableMessage:
        new_message = StableMessage(**message_data)
        self.db_session.add(new_message)
        await self.db_session.flush()
        return new_message

    async def update_message(self, message_id: int, message_data: dict) -> Union[StableMessage, None]:
        query = (
            update(StableMessage)
            .where(StableMessage.id == message_id)
            .values(message_data)
            .returning(StableMessage)
        )
        result = await self.db_session.execute(query)
        updated_message_row = result.fetchone()
        if updated_message_row:
            return updated_message_row[0]

    async def get_message_by_id(self, message_id: int) -> Union[StableMessage, None]:
        query = (
            select(StableMessage)
            .where(StableMessage.id == message_id)
            .options(joinedload(StableMessage.user))
        )
        result = await self.db_session.execute(query)
        message_row = result.fetchone()
        if message_row:
            return message_row[0]

    async def get_message_by_stable_request_id(self, stable_request_id: str) -> Union[StableMessage, None]:
        query = (
            select(StableMessage)
            .where(StableMessage.stable_request_id == stable_request_id)
            .options(joinedload(StableMessage.user))
        )
        result = await self.db_session.execute(query)
        message_row = result.fetchone()
        if message_row:
            return message_row[0]

    async def get_not_sent_to_stable_messages(self) -> list[StableMessage | None]:
        query = (
            select(StableMessage)
            .where(and_(
                StableMessage.stable_request_id == None,
                StableMessage.sent_to_stable == False,
                StableMessage.answer_sent == False,
                StableMessage.message_type == StableMessageTypeChoices.FIRST,
                StableMessage.created_at < datetime.now() - timedelta(hours=1)
            ))
            .options(
                joinedload(StableMessage.user)
                .options(joinedload(User.custom_settings))
                .options(joinedload(User.style))
            )
        )
        result = await self.db_session.execute(query)
        messages = result.fetchall()
        result = []
        for message in messages:
            result.append(message.StableMessage)
        return result
