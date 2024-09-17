from aiogram import Bot
from fastapi import APIRouter

import settings
from .stable import stable_router
from .telegram import telegram_router
from .users import user_router

main_api_router = APIRouter(prefix="/async")
main_api_router.include_router(stable_router, prefix="/stable", tags=["stable"])
main_api_router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
main_api_router.include_router(user_router, prefix="/users", tags=["users"])


@main_api_router.get("/set_webhook/")
async def on_startup():
    async with Bot(
            token=settings.main_bot_token
    ) as bot:
        await bot.set_webhook(
            url=f"{settings.SITE_DOMAIN}/async/telegram/"
        )
