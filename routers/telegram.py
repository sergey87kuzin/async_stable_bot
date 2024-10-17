from http import HTTPStatus

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_remove_reply
from database_interaction import get_db
from handlers import get_not_sent_to_stable_messages
from helpers import handle_text_message, handle_button_message, send_info_messages_all_users
from periodic_tasks import check_not_sent_to_telegram
from settings import main_bot_token

telegram_router = APIRouter()


@telegram_router.post('/')
async def handle_telegram_message(
        message: dict,
        session: AsyncSession = Depends(get_db)
):
    status = HTTPStatus.OK
    if "callback_query" in message:
        status = await handle_button_message(message.get("callback_query"), session)
    elif "message" in message:
        status = await handle_text_message(message.get("message"), session)
    return Response(status_code=status)


@telegram_router.get('/remove_reply')
async def remove_reply_command():
    await bot_remove_reply()


@telegram_router.post('/send_info_messages')
async def send_info_messages(session: AsyncSession = Depends(get_db)):
    await send_info_messages_all_users(session)


@telegram_router.post('/send_text_message')
async def send_text_message():
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN,
            ),
    ) as bot:
        await bot.send_message(chat_id=1792622682, text="some text `to copy`")


@telegram_router.post('/test_not_sent/')
async def test_not_sent(session: AsyncSession = Depends(get_db)):
    await get_not_sent_to_stable_messages(session)
