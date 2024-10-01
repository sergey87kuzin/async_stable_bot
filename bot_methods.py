import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove

from settings import main_bot_token


async def bot_send_text_message(telegram_chat_id: int, text: str, delay: float = 0) -> None:
    if delay != 0:
        await asyncio.sleep(delay)
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
    ) as bot:
        await bot.send_message(chat_id=telegram_chat_id, text=text)


async def bot_send_two_text_messages(telegram_chat_id: int, text1: str, text2: str) -> None:
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
    ) as bot:
        await bot.send_message(chat_id=telegram_chat_id, text=text1)
        await bot.send_message(chat_id=telegram_chat_id, text=text2)


async def bot_send_text_message_with_markup(telegram_chat_id: int, text: str, markup: InlineKeyboardMarkup) -> None:
    async with Bot(
        token=main_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    ) as bot:
        await bot.send_message(chat_id=telegram_chat_id, text=text, reply_markup=markup)


async def bot_edit_reply_markup(telegram_chat_id: int, message_id: int, markup: InlineKeyboardMarkup) -> None:
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            )
    ) as bot:
        await bot.edit_message_reply_markup(chat_id=telegram_chat_id, message_id=message_id, reply_markup=markup)


async def bot_send_image(
        telegram_chat_id: str,
        image_url: str,
        caption: str,
        markup: InlineKeyboardMarkup
) -> None:
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            )
    ) as bot:
        await bot.send_photo(
            chat_id=telegram_chat_id,
            photo=image_url,
            caption=caption,
            reply_markup=markup
        )


async def bot_remove_reply() -> None:
    async with Bot(token=main_bot_token) as bot:
        await bot.send_message(
            chat_id=1792622682,
            text="no_markup",
            reply_markup=ReplyKeyboardRemove()
        )
