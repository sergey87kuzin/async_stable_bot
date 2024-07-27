import os
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
from handlers import _get_user_by_username, _update_user, _create_message, _create_new_user
from handlers.site_settings import get_site_settings
from hashing import Hasher
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
            media_url = "https://ai-stocker.com/media/" + site_settings.say_hi_video
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
    pass


async def handle_text_message(message: dict, session: AsyncSession):
    chat = message.get("chat")
    if not chat:
        return ""
    telegram_chat_id = chat.get("id")
    if telegram_chat_id in BAN_LIST:
        return ""
    username = chat.get("username")
    if not username:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(chat_id=telegram_chat_id, text="У вашего аккаунта нет username")
        return ""
    initial_text = message.get("text")
    if not initial_text:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(chat_id=telegram_chat_id, text="Вы отправили пустое сообщение")
        return ""
    if initial_text == "/start":
        await handle_start_message(telegram_chat_id, username, session)
        return ""
    elif initial_text.startswith("/"):
        await handle_command(telegram_chat_id, username, initial_text, session)
    user = await _get_user_by_username(username, session)
    if not user:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(chat_id=telegram_chat_id, text="Пожалуйста, нажмите кнопку start в боте")
        return ""
    translator = GoogleTranslator(source='auto', target='en')
    answer_text = "Творим волшебство"
    if user.remain_messages > 0:
        remain_messages = user.remain_messages - 1
        await _update_user(user.id, {"remain_messages": remain_messages}, session)
    elif user.remain_messages > 0 and user.date_payment_expired >= datetime.now():
        remain_paid_messages = user.remain_paid_messages - 1
        await _update_user(user.id, {"remain_paid_messages": remain_paid_messages}, session)
    else:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(chat_id=telegram_chat_id, text="Не осталось генераций")
    await _create_message({
        "initial_text": initial_text,
        "eng_text": initial_text,
        "telegram_chat_id": str(telegram_chat_id),
        "user_id": user.id,
    }, session)


async def handle_button_message(message: dict, session: AsyncSession):
    pass
