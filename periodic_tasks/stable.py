from bot_methods import bot_send_text_message
from handlers import get_not_sent_to_stable_messages, get_no_answer_messages
from handlers.stable import send_message_to_stable, fetch_message

__all__ = (
    "check_not_sent_messages",
    "check_no_answer_message"
)

from helpers.send_to_telegram_helper import send_first_message_to_telegram


async def check_not_sent_messages(ctx: dict):
    await bot_send_text_message(1792622682, "check_not_sent_messages")
    session = ctx.get("db_session")
    not_sent_messages = await get_not_sent_to_stable_messages(session)
    for message in not_sent_messages:
        await send_message_to_stable(message, message.user, session)


async def check_no_answer_message(ctx: dict):
    await bot_send_text_message(1792622682, "check_no_answer_message")
    session = ctx.get("db_session")
    no_answer_messages = await get_no_answer_messages(session)
    for message in no_answer_messages:
        updated_message = await fetch_message(message, message.user, session)
        if updated_message:
            await send_first_message_to_telegram(updated_message, session)
