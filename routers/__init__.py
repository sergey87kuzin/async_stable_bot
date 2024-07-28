from fastapi import APIRouter

from .stable import stable_router
from .telegram import telegram_router
from .users import user_router

main_api_router = APIRouter()
main_api_router.include_router(stable_router, prefix="/stable", tags=["stable"])
main_api_router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
main_api_router.include_router(user_router, prefix="/users", tags=["users"])
