import random
from datetime import datetime

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, URLInputFile
from deep_translator import GoogleTranslator
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from ban_list import BAN_LIST
from bot_methods import bot_send_text_message
from denied_words import check_words
from handlers import _get_user_by_username, _update_user, _create_message, _create_new_user
from handlers.stable import send_message_to_stable
from handlers.site_settings import get_site_settings
from hashing import Hasher
from helpers.menu_commands import (
    instructions_handler, lessons_handler, style_handler, format_handler, order_handler,
    authorization_handler, password_handler, site_payment_handler, support_handler,
    info_handler, my_bot_handler, help_handler
)
from models import UserCreate
from settings import main_bot_token

__all__ = (
    "handle_text_message",
    "handle_button_message"
)


async def handle_start_message(telegram_chat_id: int, username: str, session: AsyncSession) -> None:
    try:
        user = await _get_user_by_username(username, session)
        if not user:
            password = Hasher.get_password_hash(str(random.randint(0, 99999999)).zfill(8))
            user_create_body = UserCreate(
                username=username,
                password=password,
                telegram_chat_id=telegram_chat_id,
            )
            user = await _create_new_user(user_create_body, session)
    except Exception as e:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(chat_id=telegram_chat_id, text="Пожалуйста, попробуйте еще раз или напишите админу")
        return
    site_settings = await get_site_settings(session)
    async with Bot(
            token=main_bot_token,
    ) as bot:
        if site_settings.say_hi_video:
            media_url = f"{settings.SITE_DOMAIN}/media/{site_settings.say_hi_video}"
            video = URLInputFile(media_url, filename=site_settings.say_hi_video)
            await bot.send_video_note(
                chat_id=telegram_chat_id,
                video_note=video
            )
        await bot.send_message(chat_id=telegram_chat_id, text="https://www.youtube.com/watch?v=PupAadTlhNQ")
        button = InlineKeyboardButton(
            text="Зарегистрироваться",
            url=f"{settings.SITE_DOMAIN}/auth/registration/{user.id}/"
        )
        register_reply_markup = InlineKeyboardMarkup(
            resize_keyboard=True,
            inline_keyboard=[[button]]
        )
        await bot.send_message(
            chat_id=telegram_chat_id,
            text="<pre>Привет ✌️ Для продолжения регистрации нажмите на кнопку:</pre>",
            reply_markup=register_reply_markup,
        )


async def handle_command(telegram_chat_id: int, username: str, command: str, session: AsyncSession) -> None:
    if command == "/instruction":
        await instructions_handler(telegram_chat_id)
    elif command == "/lessons":
        await lessons_handler(telegram_chat_id)
    elif command == "/style":
        await style_handler(telegram_chat_id, session)
    elif command == "/format":
        await format_handler(telegram_chat_id)
    elif command in ["/tariff200", "/tariff1000"]:
        await order_handler(
            telegram_chat_id=telegram_chat_id,
            order=command,
            username=username,
            session=session
        )
    elif command == "/authorization":
        await authorization_handler(telegram_chat_id=telegram_chat_id)
    elif command.startswith("/password"):
        await password_handler(
            telegram_chat_id=telegram_chat_id,
            username=username,
            password=command.replace("/password ", ""),
            session=session
        )
    elif command == "/payment":
        await site_payment_handler(telegram_chat_id=telegram_chat_id)
    elif command == "/support":
        await support_handler(telegram_chat_id=telegram_chat_id)
    elif command == "/information":
        await info_handler(telegram_chat_id=telegram_chat_id)
    elif command == "/mybot":
        await my_bot_handler(
            telegram_chat_id=telegram_chat_id,
            username=username,
            session=session
        )
    elif command == "/help":
        await help_handler(telegram_chat_id=telegram_chat_id)
    else:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Бот не обучен этой команде")


async def handle_text_message(message: dict, session: AsyncSession):
    chat = message.get("chat")
    if not chat:
        return
    telegram_chat_id = chat.get("id")
    if telegram_chat_id in BAN_LIST:
        return
    username = chat.get("username")
    if not username:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="У вашего аккаунта нет username")
        return
    initial_text = message.get("text")
    if not initial_text:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Вы отправили пустое сообщение")
        return
    if initial_text == "/start":
        await handle_start_message(telegram_chat_id, username, session)
        return
    elif initial_text.startswith("/"):
        await handle_command(telegram_chat_id, username, initial_text, session)
        return
    user = await _get_user_by_username(username, session)
    if not user:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Пожалуйста, нажмите кнопку start в боте")
        return ""
    translator = GoogleTranslator(source='auto', target='en')
    answer_text = "Творим волшебство"
    if user.remain_messages > 0:
        remain_messages = user.remain_messages - 1
        user_id = await _update_user(user.id, {"remain_messages": remain_messages}, session)
    elif user.remain_messages > 0 and user.date_payment_expired >= datetime.now():
        remain_paid_messages = user.remain_paid_messages - 1
        user_id = await _update_user(user.id, {"remain_paid_messages": remain_paid_messages}, session)
    else:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Не осталось генераций"
        )
        return
    if not user_id:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Бот косячит( пожалуйста, попробуйте снова"
        )
    # if SetVideoVariables.objects.filter(username=chat_username, is_set=False).exists():
    #     set_video_message_variables(chat_username, message_text, chat_id)
    #     return "", "", "", ""
    eng_text = translator.translate(initial_text)
    if not eng_text:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Вы отправили пустое сообщение")
        return
    wrong_words = check_words(eng_text)
    if wrong_words:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text=f"❌Вы отправили запрещенные слова: {wrong_words}"
        )
        return
    eng_text = eng_text.replace("-- ", "--").replace("blonde girl", "girl, blonde hair")
    if user.preset and user.preset not in initial_text and user.preset not in eng_text:
        initial_text = initial_text + user.preset
        eng_text = eng_text + user.preset
    # photos = message.get("photo")
    # if photos:
    #     handle_image_message.delay(eng_text, chat_id, photos, chat_username, user.id)
    #     return "", "", "", ""
    message = await _create_message({
        "initial_text": initial_text,
        "eng_text": eng_text,
        "telegram_chat_id": str(telegram_chat_id),
        "user_id": user.id,
    }, session)
    await bot_send_text_message(telegram_chat_id=telegram_chat_id, text=answer_text)
    await send_message_to_stable(message, user, session)


async def handle_button_message(message: dict, session: AsyncSession):
    pass
