import asyncio
import random
import sys
from datetime import datetime
from http import HTTPStatus

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from ban_list import BAN_LIST
from bot_methods import bot_send_text_message, bot_edit_reply_markup
from denied_words import check_words
from handlers import get_user_by_username, _update_user, _create_message, _create_new_user
from handlers.stable import send_message_to_stable, handle_vary_button, handle_repeat_button, handle_upscale_button
from handlers.site_settings import get_site_settings
from helpers.many_messages_helper import check_replays
from set_commands import set_style_handler, set_preset_handler
from handlers.users import _get_user_with_style_and_custom_settings, get_all_active_users
from hashing import Hasher
from helpers.menu_commands import (
    instructions_handler, lessons_handler, style_handler, format_handler, order_handler,
    authorization_handler, password_handler, site_payment_handler, support_handler,
    info_handler, my_bot_handler, help_handler
)
from helpers.stable import check_remains
from models import UserCreate
from settings import main_bot_token

__all__ = (
    "handle_text_message",
    "handle_button_message",
    "send_info_messages_all_users"
)


async def handle_start_message(
        telegram_chat_id: int,
        username: str,
        session: AsyncSession,
        partner_id: str = None
) -> None:
    init_password = None
    try:
        user = await get_user_by_username(username, session)
        if not user:
            init_password = str(random.randint(0, 99999999)).zfill(8)
            password = Hasher.get_password_hash(init_password)
            user_create_body = UserCreate(
                username=username,
                password=password,
                telegram_chat_id=telegram_chat_id,
                partner_id=partner_id
            )
            await _create_new_user(user_create_body, session)
    except Exception as e:
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                ),
        ) as bot:
            await bot.send_message(
                chat_id=telegram_chat_id,
                text="<pre>Пожалуйста, попробуйте еще раз или напишите админу</pre>"
            )
        return
    site_settings = await get_site_settings(session)
    async with Bot(
            token=main_bot_token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
    ) as bot:
        # if site_settings.say_hi_video:
        #     media_url = f"{settings.SITE_DOMAIN}/media/{site_settings.say_hi_video}"
        #     video = URLInputFile(media_url, filename=site_settings.say_hi_video)
        #     await bot.send_video_note(
        #         chat_id=telegram_chat_id,
        #         video_note=video
        #     )
        await bot.send_message(chat_id=telegram_chat_id, text="https://www.youtube.com/watch?v=PupAadTlhNQ")
        button = InlineKeyboardButton(
            text="Посмотреть уроки",
            url=f"{settings.SITE_DOMAIN}/courses/course/2"
        )
        register_reply_markup = InlineKeyboardMarkup(
            resize_keyboard=True,
            inline_keyboard=[[button]]
        )
        await bot.send_message(
            chat_id=telegram_chat_id,
            text="<pre>Привет ✌️ Уроки о продаже работ в интернете доступны по кнопке ниже:</pre>",
            reply_markup=register_reply_markup,
        )
        if init_password:
            await bot.send_message(
                chat_id=telegram_chat_id,
                text=f"<pre>Ваш логин {username} \nВаш пароль {init_password}</pre>",
                reply_markup=register_reply_markup,
            )


async def handle_command(telegram_chat_id: int, username: str, command: str, session: AsyncSession) -> int:
    if command == "/instruction":
        await instructions_handler(telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/lessons":
        await lessons_handler(telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/style":
        await style_handler(telegram_chat_id, session)
        return HTTPStatus.OK
    elif command == "/format":
        await format_handler(telegram_chat_id)
        return HTTPStatus.OK
    elif command in ["/tariff200", "/tariff1000"]:
        await order_handler(
            telegram_chat_id=telegram_chat_id,
            order=command,
            username=username,
            session=session
        )
        return HTTPStatus.OK
    elif command == "/authorization":
        await authorization_handler(telegram_chat_id=telegram_chat_id)
        return HTTPStatus.OK
    elif command.startswith("/password"):
        if command == "/password":
            await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Вы забыли указать пароль")
            return HTTPStatus.NO_CONTENT
        await password_handler(
            telegram_chat_id=telegram_chat_id,
            username=username,
            password=command.replace("/password ", ""),
            session=session
        )
        return HTTPStatus.OK
    elif command == "/payment":
        await site_payment_handler(telegram_chat_id=telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/support":
        await support_handler(telegram_chat_id=telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/information":
        await info_handler(telegram_chat_id=telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/mybot":
        await my_bot_handler(
            telegram_chat_id=telegram_chat_id,
            username=username,
            session=session
        )
        return HTTPStatus.OK
    elif command == "/help":
        await help_handler(telegram_chat_id=telegram_chat_id)
        return HTTPStatus.OK
    elif command == "/referal":
        async with Bot(
                token=main_bot_token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.MARKDOWN,
                ),
        ) as bot:
            await bot.send_message(
                chat_id=telegram_chat_id,
                text=f"""Для того, чтобы скопировать ссылку, нажмите на нее: \n
                 `https://t.me/@ToMidjourneyBot?start={telegram_chat_id}`"""
            )
        return HTTPStatus.OK
    else:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Бот не обучен этой команде")
        return HTTPStatus.NO_CONTENT


async def handle_text_message(message: dict, session: AsyncSession) -> int:
    chat = message.get("chat")
    if not chat:
        return HTTPStatus.NO_CONTENT
    telegram_chat_id = chat.get("id")
    if telegram_chat_id in BAN_LIST:
        return HTTPStatus.NO_CONTENT
    username = chat.get("username")
    if not username:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="У вашего аккаунта нет username")
        return HTTPStatus.NO_CONTENT
    initial_text = message.get("text")
    if not initial_text:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Вы отправили пустое сообщение")
        return HTTPStatus.NO_CONTENT
    if initial_text.startswith("/start"):
        start_data = initial_text.split(" ")
        partner_id = None
        if start_data[0] == "/start" and len(start_data) == 2:
            partner_id = start_data[1]
        await handle_start_message(telegram_chat_id, username, session, partner_id)
        return HTTPStatus.OK
    elif initial_text.startswith("/"):
        status = await handle_command(telegram_chat_id, username, initial_text, session)
        return status
    user = await _get_user_with_style_and_custom_settings(username, session)
    if not user:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Пожалуйста, нажмите кнопку start в боте")
        return HTTPStatus.NO_CONTENT
    translator = GoogleTranslator(source='auto', target='en')
    answer_text = "Творим волшебство"
    if user.remain_messages > 0:
        remain_messages = user.remain_messages - 1
        user_id = await _update_user(user.id, {"remain_messages": remain_messages}, session)
    elif user.remain_paid_messages > 0 and user.date_payment_expired.replace(tzinfo=None) >= datetime.now():
        remain_paid_messages = user.remain_paid_messages - 1
        user_id = await _update_user(user.id, {"remain_paid_messages": remain_paid_messages}, session)
    else:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Не осталось генераций"
        )
        return HTTPStatus.NO_CONTENT
    if not user_id:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text="Бот косячит( пожалуйста, попробуйте снова"
        )
        return HTTPStatus.NO_CONTENT
    # if SetVideoVariables.objects.filter(username=chat_username, is_set=False).exists():
    #     set_video_message_variables(chat_username, message_text, chat_id)
    #     return "", "", "", ""
    eng_text = translator.translate(initial_text)
    if not eng_text:
        await bot_send_text_message(telegram_chat_id=telegram_chat_id, text="Вы отправили пустое сообщение")
        return HTTPStatus.NO_CONTENT
    wrong_words = check_words(eng_text)
    if wrong_words:
        await bot_send_text_message(
            telegram_chat_id=telegram_chat_id,
            text=f"❌Вы отправили запрещенные слова: {wrong_words}"
        )
        return HTTPStatus.NO_CONTENT
    eng_text = eng_text.replace("-- ", "--").replace("blonde girl", "girl, blonde hair")
    if user.preset and user.preset not in initial_text and user.preset not in eng_text:
        initial_text = initial_text + user.preset
        eng_text = eng_text + user.preset
    # photos = message.get("photo")
    # if photos:
    #     handle_image_message.delay(eng_text, chat_id, photos, chat_username, user.id)
    #     return "", "", "", ""
    if user.is_test_user:
        many_words_eng_text = check_replays(eng_text)
        if many_words_eng_text:
            tasks = []
            for index, new_prompt in enumerate(many_words_eng_text):
                message = await _create_message({
                    "initial_text": new_prompt,
                    "eng_text": new_prompt,
                    "telegram_chat_id": str(telegram_chat_id),
                    "user_id": user.id,
                    "created_at": datetime.now()
                }, session)
                await bot_send_text_message(
                    telegram_chat_id=telegram_chat_id,
                    text=f"{answer_text} - Генерация по запросу: {new_prompt}"
                )
                task = send_message_to_stable(
                    message=message,
                    user=user,
                    session=session,
                    pause_time=int(index)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)
            return HTTPStatus.OK
    message = await _create_message({
        "initial_text": initial_text,
        "eng_text": eng_text,
        "telegram_chat_id": str(telegram_chat_id),
        "user_id": user.id,
        "created_at": datetime.now(),
    }, session)
    await bot_send_text_message(
        telegram_chat_id=telegram_chat_id,
        text=f"{answer_text} - Генерация по запросу: {initial_text}"
    )
    if "pytest" not in sys.modules:
        task = send_message_to_stable(message, user, session)
        asyncio.create_task(task)
        # background_tasks.add_task(send_message_to_stable, message, user, session)
    return HTTPStatus.OK


async def handle_button_message(button_data: dict, session: AsyncSession) -> int:
    if button_data:
        chat_id = button_data.get("from", {}).get("id")
        if chat_id in BAN_LIST:
            return HTTPStatus.NO_CONTENT
        message_text = button_data.get("data")
        # if StableMessage.objects.filter(
        #         eng_text=message_text,
        #         created_at__gt=datetime.now() - timedelta(minutes=1)
        # ).exists():
        #     await bot_send_text_message(telegram_chat_id=chat_id, text="Вы уже нажимали на эту кнопку)")
        #     return
        chat_username = button_data.get("from", {}).get("username")
        user = await _get_user_with_style_and_custom_settings(chat_username, session)
        if not user:
            await bot_send_text_message(telegram_chat_id=chat_id, text="Вы не зарегистрированы в приложении")
            return HTTPStatus.NO_CONTENT
        if message_text.startswith("preset&&"):
            preset_name = message_text.replace("preset&&", "")
            await set_preset_handler(user, preset_name, session)
            return HTTPStatus.OK
        if message_text.startswith("style&&"):
            style_name = message_text.replace("style&&", "")
            status = await set_style_handler(user, style_name, session)
            return status
        # Пр нажатии на кнопку заменяем ее на символ нажатия
        reply_markup = button_data.get("message").get("reply_markup")
        buttons = [[]]
        for line in reply_markup.get("inline_keyboard"):
            line_buttons = []
            for button in line:
                if button.get("callback_data") == button_data.get("data"):
                    item = InlineKeyboardButton(
                        text="✅",
                        callback_data=button.get("callback_data")
                    )
                else:
                    item = InlineKeyboardButton(
                        text=button.get("text"),
                        callback_data=button.get("callback_data")
                    )
                line_buttons.append(item)
            buttons.append(line_buttons)
        buttons_markup = InlineKeyboardMarkup(
            resize_keyboard=True,
            inline_keyboard=buttons
        )
        try:
            await bot_edit_reply_markup(
                message_id=button_data.get("message").get("message_id"),
                markup=buttons_markup,
                telegram_chat_id=chat_id
            )
        except Exception:
            pass
        if not message_text or not chat_username or not chat_id:
            await bot_send_text_message(telegram_chat_id=chat_id, text="С этой кнопкой что-то не так")
            return HTTPStatus.NO_CONTENT
        eng_text = message_text
        if not await check_remains(eng_text, user, chat_id, session):
            return HTTPStatus.NO_CONTENT
        if message_text.startswith("button_visualize&&"):
            if user.remain_video_messages <= 0:
                await bot_send_text_message(
                    telegram_chat_id=chat_id,
                    text="У вас закончились видео генерации"
                )
                return HTTPStatus.NO_CONTENT
            # handle_visualize_button(message_text, user, chat_id)
            return HTTPStatus.OK
        elif message_text.startswith("button_upscale"):
            await handle_upscale_button(message_text, chat_id, session)
            return HTTPStatus.OK
        # elif message_text.startswith("button_zoom&&"):
        #     handle_zoom_button(message_text, chat_id, "back")
        #     return
        # elif message_text.startswith("button_move"):
        #     direction = message_text.split("&&")[1]
        #     handle_zoom_button(message_text, chat_id, direction)
        #     return
        if message_text.startswith("button_vary&&"):
            await handle_vary_button(message_text, chat_id, session)
        elif message_text.startswith("button_send_again&&"):
            await handle_repeat_button(message_text, chat_id, session)
        return HTTPStatus.OK
    else:
        # user = User.objects.first()
        # stable_bot.send_message(
        #     chat_id=user.chat_id,
        #     text="Кто-то опять косячит :)",
        # )
        return HTTPStatus.NO_CONTENT


async def send_info_messages_all_users(session: AsyncSession) -> None:
    users = await get_all_active_users(session)
    site_settings = await get_site_settings(session)
    all_tasks = []
    for index, user in enumerate(users):
        task = bot_send_text_message(
            user.chat_id,
            text=site_settings.notice_message,
            delay=1 * index
        )
        all_tasks.append(task)
    await asyncio.gather(*all_tasks)
