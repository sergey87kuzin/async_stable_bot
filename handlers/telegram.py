from sqlalchemy.ext.asyncio import AsyncSession

from global_constants import StableMessageTypeChoices
from handlers import get_message_by_id
from helpers.send_to_telegram_helper import send_first_message_to_telegram


async def send_images_to_telegram(message_id: int, session: AsyncSession):
    print("Отправляю таски в телегу")
    message = await get_message_by_id(message_id, session)
    if message.answer_sent:
        return
    if message.message_type == StableMessageTypeChoices.FIRST:
        await send_first_message_to_telegram(message, session)
