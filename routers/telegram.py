from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from database_interaction import get_db
from helpers import handle_text_message, handle_button_message

telegram_router = APIRouter()


@telegram_router.post('/')
async def handle_telegram_message(message: dict, session: AsyncSession = Depends(get_db)):
    if "text" in message:
        await handle_text_message(message, session)
    elif "callback_query" in message:
        await handle_button_message(message.get("callback_query"), session)
    return Response(status_code=HTTPStatus.OK)
