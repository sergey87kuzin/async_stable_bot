from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_text_message, bot_send_two_text_messages, bot_send_text_message_with_markup
from helpers.menu_texts import PRESET_INFO_TEXT, STYLE_INFO_TEXT, MENU_INFORMATION_TEXT, INFO_TEXT, PASSWORD_TEXT, \
    SUPPORT_TEXT, PAYMENT_TEXT
from settings import SITE_DOMAIN

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
    "password_handler",
    "help_handler"
)


async def format_handler(telegram_chat_id: int) -> None:
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=PRESET_INFO_TEXT)


async def style_handler(telegram_chat_id: int) -> None:
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=STYLE_INFO_TEXT)


async def order_handler(telegram_chat_id: int, order: str, username: str, session: AsyncSession) -> None:
    pass


async def my_bot_handler(telegram_chat_id: int, username: str, session: AsyncSession) -> None:
    pass


async def info_handler(telegram_chat_id: int) -> None:
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=MENU_INFORMATION_TEXT)


async def instructions_handler(telegram_chat_id: int) -> None:
    info_button = InlineKeyboardButton(
        text="Перейти на сайт",
        url=f"{SITE_DOMAIN}/courses/course/2/"
    )
    info_markup = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[[info_button]]
    )
    await bot_send_text_message_with_markup(
        telegram_chat_id=telegram_chat_id,
        text=INFO_TEXT,
        markup=info_markup
    )


async def lessons_handler(telegram_chat_id: int) -> None:
    text = f"{SITE_DOMAIN}/courses/course/2/"
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=text)


async def authorization_handler(telegram_chat_id: int) -> None:
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=PASSWORD_TEXT)


async def site_payment_handler(telegram_chat_id: int) -> None:
    await bot_send_two_text_messages(
        telegram_chat_id=telegram_chat_id,
        text1=PAYMENT_TEXT,
        text2=f"{SITE_DOMAIN}/payments-page/"
    )


async def support_handler(telegram_chat_id: int) -> None:
    await bot_send_two_text_messages(
        telegram_chat_id=telegram_chat_id,
        text1=SUPPORT_TEXT,
        text2="@ai_stocker_help_bot"
    )


async def password_handler(telegram_chat_id: int, username: str, password: str, session: AsyncSession) -> None:
    pass


async def help_handler(telegram_chat_id: int) -> None:
    text: str = f"""<pre>▪️ Для того, чтобы начать генерацию, просто вводите текст промпта\n\n▪️ Вы можете отправлять следующее сообщение боту, не дожидаясь изображения на предыдущий запрос\n\n▪️ Для того, чтобы поменять пароль, введите:\n/password и новый пароль\n\n▪️ Переход на сайт:\n {SITE_DOMAIN}</pre>""",
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="".join(text))
