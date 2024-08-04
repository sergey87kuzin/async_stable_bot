from bot_methods import bot_send_text_message
from handlers import get_not_sent_to_stable_messages
from handlers.stable import send_message_to_stable

__all__ = (
    "check_not_sent_messages",
)


async def check_not_sent_messages(ctx: dict):
    await bot_send_text_message(1792622682, "success")
    session = ctx.get("db_session")
    not_sent_messages = await get_not_sent_to_stable_messages(session)
    for message in not_sent_messages:
        await send_message_to_stable(message, message.user, session)
