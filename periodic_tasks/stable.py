import asyncio

from bot_methods import bot_send_text_message
from global_constants import StableMessageTypeChoices
from handlers import get_not_sent_to_stable_messages, get_no_answer_messages
from handlers.stable import send_message_to_stable, fetch_message, send_upscale_to_stable

__all__ = (
    "check_not_sent_messages",
    "check_no_answer_message"
)

from helpers.send_to_telegram_helper import send_first_message_to_telegram


async def check_not_sent_messages(ctx: dict):
    await bot_send_text_message(1792622682, "check_not_sent_messages")
    session = ctx.get("db_session")
    not_sent_messages = await get_not_sent_to_stable_messages(session)
    tasks = []
    for index, message in enumerate(not_sent_messages):
        if message.message_type == StableMessageTypeChoices.FIRST:
            task = send_message_to_stable(message, message.user, session, pause_time=int(index))
            tasks.append(task)
        elif message.message_type == StableMessageTypeChoices.UPSCALED:
            task = send_upscale_to_stable(message, message.user, session)
            tasks.append(task)
    await asyncio.gather(*tasks)


async def check_no_answer_message(ctx: dict):
    await bot_send_text_message(1792622682, "check_no_answer_message")
    session = ctx.get("db_session")
    no_answer_messages = await get_no_answer_messages(session)
    for message in no_answer_messages:
        updated_message = await fetch_message(message, message.user, session)
        if updated_message:
            if message.message_type == StableMessageTypeChoices.FIRST:
                await send_message_to_stable(message, message.user, session)
            elif message.message_type == StableMessageTypeChoices.UPSCALED:
                await send_upscale_to_stable(message, message.user, session)
