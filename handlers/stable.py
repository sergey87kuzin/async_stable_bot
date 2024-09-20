import asyncio
import json
import sys
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from async_requests import post
from bot_methods import bot_send_text_message
from global_constants import StableMessageTypeChoices
from handlers import get_message_by_id, _create_message, get_stable_settings, _get_user_with_style_and_custom_settings, \
    _update_user, _update_message
from schemas import StableMessage, User
from settings import STABLE_API_KEY

headers = {
    'Content-Type': 'application/json'
}


async def send_message_to_stable(
        message: StableMessage,
        user: User,
        session: AsyncSession,
        main_callback_url: bool = False
):
    """https://docs.modelslab.com/image-generation/community-models/dreamboothtext2img"""
    from helpers import get_stable_data, handle_stable_text2img_answer
    stable_settings = await get_stable_settings(session)
    data = await get_stable_data(
        message,
        user,
        stable_settings,
        session,
        main_callback_url
    )

    text_message_url = "https://modelslab.com/api/v6/images/text2img"
    response_data = await post(text_message_url, headers=headers, data=json.dumps(data))

    remain_messages = user.remain_messages + 1
    if response_data:
        await handle_stable_text2img_answer(response_data, message, remain_messages, session)
    else:
        await _update_user(user_id=user.id, update_data={"remain_messages": remain_messages}, session=session)
        await _update_message(message_id=message.id, update_data={"answer_sent": True}, session=session)
        await bot_send_text_message(
            telegram_chat_id=message.telegram_chat_id,
            text=f"<pre>Ошибка создания сообщения. {message.eng_text}. Вам добавлена одна генерация</pre>"
        )


async def fetch_message(message: StableMessage, user: User, session: AsyncSession) -> Union[StableMessage, None]:
    """https://docs.modelslab.com/image-generation/community-models/dreamboothfetchqueimg"""
    from helpers import handle_stable_fetch_answer
    data = {
        "key": STABLE_API_KEY,
        "request_id": message.stable_request_id
    }
    fetch_url = "https://modelslab.com/api/v6/images/fetch"
    response_data = await post(fetch_url, headers=headers, data=json.dumps(data))

    if response_data:
        remain_messages = user.remain_messages + 1
        updated_message = await handle_stable_fetch_answer(response_data, message, remain_messages, session)
        if updated_message:
            return updated_message


async def send_vary_to_stable(message: StableMessage, user: User, session: AsyncSession):
    """https://docs.modelslab.com/image-generation/community-models/dreamboothtext2img"""
    from helpers import get_stable_data, handle_stable_text2img_answer
    # на данный момент не работает с нашей моделью
    stable_settings = await get_stable_settings(session)
    data = await get_stable_data(message, user, stable_settings, session)
    data["ip_adapter_id"] = "ip-adapter_sdxl"
    data["ip_adapter_scale"] = 0.7
    data["ip_adapter_image"] = message.first_image

    text_message_url = "https://modelslab.com/api/v6/images/text2img"
    response_data = await post(text_message_url, headers=headers, data=json.dumps(data))

    if response_data:
        remain_messages = user.remain_messages + 1
        await handle_stable_text2img_answer(response_data, message, remain_messages, session)
    else:
        await bot_send_text_message(
            telegram_chat_id=message.telegram_chat_id,
            text=f"<pre>Ошибка создания вариаций. {message.eng_text}. Вам добавлена одна генерация</pre>"
        )


async def handle_vary_button(
        message_text: str,
        chat_id: int,
        session: AsyncSession,
):
    initial_message_id = int(message_text.split("&&")[-1])
    initial_message = await get_message_by_id(initial_message_id, session)
    user = initial_message.user
    created_message = await _create_message({
        "initial_text": initial_message.initial_text,
        "eng_text": initial_message.initial_text,
        "telegram_chat_id": str(chat_id),
        "user_id": user.id,
        "first_image": initial_message.single_image,
        "message_type": StableMessageTypeChoices.VARY
    }, session)
    answer_text = "Делаем вариации"
    await bot_send_text_message(telegram_chat_id=chat_id, text=answer_text)
    if "pytest" not in sys.modules:
        task = send_vary_to_stable(created_message, user, session)
        asyncio.create_task(task)
        # background_tasks.add_task(send_vary_to_stable, created_message, user, session)


async def handle_repeat_button(
        message_text: str,
        chat_id: int,
        session: AsyncSession
):
    initial_message_id = int(message_text.split("&&")[-1])
    initial_message = await get_message_by_id(initial_message_id, session)
    user = await _get_user_with_style_and_custom_settings(
        initial_message.user.username,
        session
    )
    created_message = await _create_message({
        "initial_text": initial_message.initial_text,
        "eng_text": initial_message.initial_text,
        "telegram_chat_id": str(chat_id),
        "user_id": user.id,
        "message_type": StableMessageTypeChoices.FIRST
    }, session)
    answer_text = "Творим волшебство"
    await bot_send_text_message(telegram_chat_id=chat_id, text=answer_text)
    if "pytest" not in sys.modules:
        task = send_message_to_stable(created_message, user, session)
        asyncio.create_task(task)
        # background_tasks.add_task(send_message_to_stable, created_message, user, session)
