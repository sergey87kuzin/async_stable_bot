from bot_methods import bot_send_text_message
from handlers import get_not_sent_to_telegram_messages
from helpers.send_to_telegram_helper import send_first_message_to_telegram

__all__ = (
    "check_not_sent_to_telegram",
)


async def check_not_sent_to_telegram(ctx: dict):
    await bot_send_text_message(1792622682, "check_not_sent_to_telegram")
    session = ctx.get("db_session")
    not_sent_messages = await get_not_sent_to_telegram_messages(session)
    for message in not_sent_messages:
        await send_first_message_to_telegram(message, session)
