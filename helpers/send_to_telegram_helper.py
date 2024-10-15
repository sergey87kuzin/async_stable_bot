from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_image, bot_send_text_message, bot_send_text_message_with_markup
from global_constants import StableMessageTypeChoices
from handlers import _create_message, _update_message
from schemas import StableMessage


def generate_image_message_keyboard(message_id: int) -> InlineKeyboardMarkup:
    buttons_data = (
        # ("⬅️", f"button_move&&left&&{message_id}"),
        # ("➡️", f"button_move&&right&&{message_id}"),
        # ("⬆️", f"button_move&&up&&{message_id}"),
        # ("⬇️", f"button_move&&down&&{message_id}"),
        # ("🔍", f"button_zoom&&{message_id}"),
        ("4️⃣x", f"button_upscale&&{message_id}"),
        # ("🔢", f"button_vary&&{message_id}"),
        # ("🎦", f"button_visualize&&{message_id}"),
        ("🔄", f"button_send_again&&{message_id}"),
    )
    buttons_row = []
    for button_data in buttons_data:
        button = InlineKeyboardButton(
            text=button_data[0],
            callback_data=button_data[1]
        )
        buttons_row.append(button)
    return InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[buttons_row]
    )


async def send_first_message_to_telegram(message: StableMessage, session: AsyncSession) -> None:
    images = {
        "U1": message.first_image,
        "U2": message.second_image,
        "U3": message.third_image,
        "U4": message.fourth_image
    }
    for button_name, image in images.items():
        if not image:
            continue
        message_data = {
            "initial_text": message.eng_text,
            "eng_text": f"button_u&&{button_name}&&{message.id}",
            "telegram_chat_id": message.telegram_chat_id,
            "user_id": message.user_id,
            "single_image": image,
            "answer_sent": True,
            "message_type": StableMessageTypeChoices.U,
            "width": message.width,
            "height": message.height,
            "seed": message.seed
        }
        new_message = await _create_message(message_data, session)
        buttons_u_markup = generate_image_message_keyboard(new_message.id)
        try:
            await bot_send_image(
                telegram_chat_id=message.telegram_chat_id,
                image_url=new_message.single_image,
                caption=new_message.initial_text,
                markup=buttons_u_markup
            )
        except Exception:
            await bot_send_text_message(
                telegram_chat_id=new_message.telegram_chat_id,
                text=f"<a href='{image}'>Скачайте увеличенное фото тут</a>"
            )
            await bot_send_text_message_with_markup(
                telegram_chat_id=new_message.telegram_chat_id,
                text=new_message.initial_text,
                markup=buttons_u_markup
            )
    message_data = {"answer_sent": True}
    await _update_message(message.id, message_data, session)
    with open("log.txt", "a") as log:
        log.write(f"callback handled successfully {message.id}\n")


async def send_upscaled_message_to_telegram(message: StableMessage, session: AsyncSession) -> None:
    await bot_send_text_message(
        telegram_chat_id=message.telegram_chat_id,
        text=f"<a href='{message.single_image}'>Скачайте увеличенное фото тут</a>"
    )
    await bot_send_text_message(
        telegram_chat_id=message.telegram_chat_id,
        text=f"4х: {message.initial_text}"
    )
    message_data = {"answer_sent": True}
    await _update_message(message.id, message_data, session)
