from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_text_message
from handlers import _update_user
from handlers.style import get_style_by_name
from schemas import User


async def set_style_handler(user: User, style_name: str, session: AsyncSession) -> int:
    if style_name == "info":
        style = user.style
        if not style:
            await bot_send_text_message(user.chat_id, "Стиль не установлен")
            status = HTTPStatus.NO_CONTENT
        else:
            await bot_send_text_message(user.chat_id, f"Ваш стиль {style.name_for_menu}")
            status = HTTPStatus.OK
    elif style_name == "del":
        await _update_user(user.id, {"style_id": None}, session)
        await bot_send_text_message(user.chat_id, f"Стиль удален")
        status = HTTPStatus.OK
    else:
        style = await get_style_by_name(style_name, session)
        if not style:
            status = HTTPStatus.NO_CONTENT
        else:
            await _update_user(user.id, {"style_id": style.id}, session)
            await bot_send_text_message(user.chat_id, f"Ваш стиль {style.name_for_menu}")
            status = HTTPStatus.OK
    return status


async def set_preset_handler(user: User, preset: str, session: AsyncSession) -> int:
    if preset == "info":
        user_preset = user.preset.replace(" --ar ", "") if user.preset else "Не установлен"
        await bot_send_text_message(user.chat_id, f"Ваш стиль {user_preset}")
        status = HTTPStatus.OK
    elif preset == "del":
        await _update_user(user.id, {"preset": None}, session)
        await bot_send_text_message(user.chat_id, "Формат удален")
        status = HTTPStatus.OK
    else:
        await _update_user(user.id, {"preset": preset}, session)
        await bot_send_text_message(user.chat_id, f"Формат установлен на {preset.replace(' --ar ', '')}")
        status = HTTPStatus.OK
    return status
