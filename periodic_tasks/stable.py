from sqlalchemy.ext.asyncio import AsyncSession

from handlers import get_not_sent_to_stable_messages
from handlers.stable import send_message_to_stable

__all__ = (
    "check_not_sent_messages",
)


async def check_not_sent_messages(session: AsyncSession):
    not_sent_messages = await get_not_sent_to_stable_messages(session)
    for message in not_sent_messages:
        await send_message_to_stable(message, message.user, session)
