from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup

from settings import main_bot_token


async def bot_send_text_message(telegram_chat_id: int, text: str) -> None:
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
