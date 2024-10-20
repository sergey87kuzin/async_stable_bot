from cachetools import TTLCache

from http import HTTPStatus

import asyncio
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_text_message
from database_interaction import get_db
from handlers import _update_message, get_message_by_stable_request_id, _update_user
from handlers.telegram import send_images_to_telegram

stable_router = APIRouter()
cache = TTLCache(maxsize=128, ttl=60)


@stable_router.post("/stable_webhook/")
async def stable_image_webhook(
        data: dict,
        session: AsyncSession = Depends(get_db)

):
    images = data.get("output")
    message_id = data.get("track_id")
    if images and data.get("status") == "success":
        item = cache.get(message_id, None)
        if item is not None:
            return Response(status_code=HTTPStatus.OK)
        else:
            cache[message_id] = True
        # if user.is_test_user and message.message_type == StableMessageTypeChoices.DOUBLE:
        #     message.first_image = images[0]
        #     message.message_type = StableMessageTypeChoices.FIRST
        #     message.save()
        #     send_vary_to_stable_new.apply_async([message.id], countdown=3)
        #     return Response(status=HTTPStatus.OK)
        message_data = {"single_image": images[0]}
        try:
            message_data["first_image"] = images[0]
            message_data["second_image"] = images[1]
            message_data["third_image"] = images[2]
            message_data["fourth_image"] = images[3]
        except Exception:
            print("wrong one")
        await _update_message(message_id=message_id, update_data=message_data, session=session)
        task = send_images_to_telegram(message_id, session)
        asyncio.create_task(task)
        with open("log.txt", "a") as log:
            log.write(f"success callback {message_id}\n")
    if data.get("status") in ("failed", "error"):
        item = cache.get(message_id, None)
        if item is not None:
            return Response(status_code=HTTPStatus.OK)
        else:
            cache[message_id] = True
        message = await get_message_by_stable_request_id(stable_request_id=str(data.get("id")), session=session)
        if message:
            user = message.user
            await bot_send_text_message(
                telegram_chat_id=message.telegram_chat_id,
                text=f"<pre>❌Ошибка генерации/n✅ вам добавлена 1 генерация, отправьте запрос заново {message.initial_text}</pre>"
            )
            message_data = {"answer_sent": True}
            await _update_message(message.id, message_data, session)
            user_data = {"remain_messages": user.remain_messages + 1}
            await _update_user(user.id, user_data, session)
    return Response(status_code=HTTPStatus.OK)


@stable_router.post("/stable_upscale_webhook/")
async def stable_image_webhook(
        data: dict,
        session: AsyncSession = Depends(get_db)
):
    images = data.get("output")
    message_id = int(data.get("track_id"))

    if images and data.get("status") == "success":
        item = cache.get(message_id, None)
        if item is not None:
            return Response(status_code=HTTPStatus.OK)
        else:
            cache[message_id] = True
        message_data = {"single_image": images[0]}
        await _update_message(message_id=message_id, update_data=message_data, session=session)
        task = send_images_to_telegram(message_id, session)
        asyncio.create_task(task)
    if data.get("status") in ("failed", "error"):
        item = cache.get(message_id, None)
        if item is not None:
            return Response(status_code=HTTPStatus.OK)
        else:
            cache[message_id] = True
        message = await get_message_by_stable_request_id(stable_request_id=str(data.get("id")), session=session)
        if message:
            user = message.user
            await bot_send_text_message(
                telegram_chat_id=message.telegram_chat_id,
                text=f"Ошибка увеличения {message.initial_text}. Вам добавлена одна генерация"
            )
            message_data = {"answer_sent": True}
            await _update_message(message.id, message_data, session)
            user_data = {"remain_messages": user.remain_messages + 1}
            await _update_user(user.id, user_data, session)
    return Response(status_code=HTTPStatus.OK)
