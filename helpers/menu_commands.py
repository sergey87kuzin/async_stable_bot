from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_text_message, bot_send_two_text_messages, bot_send_text_message_with_markup
from dals import UserDAL
from dals.style_dal import StyleDAL
from handlers import _get_user_by_username
from helpers.menu_texts import PRESET_INFO_TEXT, STYLE_INFO_TEXT, MENU_INFORMATION_TEXT, INFO_TEXT, PASSWORD_TEXT, \
    SUPPORT_TEXT, PAYMENT_TEXT
from helpers.orders import create_order_from_menu
from schemas import Order
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
    first_line_presets = (
        ("3:2", " --ar 3:2"),
        ("2:3", " --ar 2:3"),
        ("16:9", " --ar 16:9"),
        ("9:16", " --ar 9:16"),
    )
    second_line_presets = (
        ("3:1", " --ar 3:1"),
        ("Удалить", "preset&&del"),
        ("Инфо", "preset&&info")
    )
    first_line_buttons = []
    second_line_buttons = []
    for preset in first_line_presets:
        format_button = InlineKeyboardButton(
            text=preset[0],
            callback_data=f"preset&&{preset[1]}"
        )
        first_line_buttons.append(format_button)
    for preset in second_line_presets:
        format_button = InlineKeyboardButton(
            text=preset[0],
            callback_data=f"preset&&{preset[1]}"
        )
        second_line_buttons.append(format_button)
    format_markup = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[first_line_buttons, second_line_buttons]
    )
    await bot_send_text_message_with_markup(
        telegram_chat_id=telegram_chat_id,
        text=PRESET_INFO_TEXT,
        markup=format_markup
    )


async def style_handler(telegram_chat_id: int, session: AsyncSession) -> None:
    styles = await StyleDAL(session).get_all_styles()
    style_buttons = []
    for style in styles:
        style_buttons.append([InlineKeyboardButton(
            text=style.name_for_menu,
            callback_data=f"style&&{style.name}"
        )])
    style_buttons.append([InlineKeyboardButton(
        text="Удалить",
        callback_data=f"style&&del"
    )])
    style_buttons.append([InlineKeyboardButton(
        text="Инфо ℹ️",
        callback_data=f"style&&info"
    )])
    style_markup = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=style_buttons
    )
    await bot_send_text_message_with_markup(
        telegram_chat_id=telegram_chat_id,
        text=STYLE_INFO_TEXT,
        markup=style_markup
    )


async def order_handler(telegram_chat_id: int, order: str, username: str, session: AsyncSession) -> None:
    user = await _get_user_by_username(username=username, session=session)
    if not user:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Ваш бот не найден. Пожалуйста, обратитесь в поддержку"
        )
        return
    payment_url = ""
    if order == "/tariff200":
        payment_url = await create_order_from_menu("day", user, session)
    elif order == "/tariff1000":
        payment_url = await create_order_from_menu("month", user, session)
    if not payment_url:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Невозможно создать ссылку, обратитесь в техподдержку"
        )
        return
    await bot_send_two_text_messages(
        telegram_chat_id=telegram_chat_id,
        text1="""<pre>Если у вас еще остались генерации, они сгорят при покупке новых.
                 Не покупайте новые генерации, пока не израсходуете предыдущие</pre>""",
        text2=f"<a href='{payment_url}'>Ссылка на оплату</a>"
    )


async def my_bot_handler(telegram_chat_id: int, username: str, session: AsyncSession) -> None:
    user = await UserDAL(session).get_user_by_username(username)
    if not user:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Ваш бот не найден. Пожалуйста, обратитесь в поддержку"
        )
        return
    my_bot_text = f"""<pre>Доступ до: {user.get_bot_end}\n\nДоступные генерации: {user.all_messages}\n</pre>"""
    extend_button = InlineKeyboardButton(
        text="Продлить",
        url=SITE_DOMAIN
    )
    my_bot_markup = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[[extend_button]]
    )
    await bot_send_text_message_with_markup(
        telegram_chat_id=telegram_chat_id,
        text=my_bot_text,
        markup=my_bot_markup
    )


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
