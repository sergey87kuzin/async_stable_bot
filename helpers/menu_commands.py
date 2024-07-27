from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "instructions_handler",
    "format_handler",
    "style_handler",
    "order_handler",
    "my_bot_handler",
    "info_handler",
    "lessons_handler",
    "authorization_handler",
    "site_payment_handler",
    "support_handler",
    "password_handler"
)


async def format_handler(telegram_chat_id: int) -> None:
    pass


async def style_handler(telegram_chat_id: int) -> None:
    pass


async def order_handler(telegram_chat_id: int, order: str, username: str, session: AsyncSession) -> None:
    pass


async def my_bot_handler(telegram_chat_id: int, username: str, session: AsyncSession) -> None:
    pass


async def info_handler(telegram_chat_id: int) -> None:
    pass


async def instructions_handler(telegram_chat_id: int) -> None:
    pass


async def lessons_handler(telegram_chat_id: int) -> None:
    pass


async def authorization_handler(telegram_chat_id: int) -> None:
    pass


async def site_payment_handler(telegram_chat_id: int) -> None:
    pass


async def support_handler(telegram_chat_id: int) -> None:
    pass


async def password_handler(telegram_chat_id: int, username: str, password: str, session: AsyncSession) -> None:
    pass
