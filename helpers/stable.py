from datetime import datetime, date
from random import randint
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from bot_methods import bot_send_text_message
from global_constants import SCALES
from handlers import _update_message, _update_user
from schemas import StableMessage, User, StableSettings
from settings import STABLE_API_KEY, SITE_DOMAIN


__all__ = (
    "get_stable_data",
    "handle_stable_text2img_answer",
    "check_remains",
    "handle_stable_fetch_answer",
    "handle_stable_upscale_answer"
)


def get_sizes(scale):
    result = ("1024", "1024")
    return SCALES.get(scale) or result


def get_user_prompts(
        eng_text,
        style_positive_prompt: Union[str, None] = None,
        style_negative_prompt: Union[str, None] = None,
        custom_settings_positive_prompt: Union[str, None] = None,
        custom_settings_negative_prompt: Union[str, None] = None,
        stable_settings_positive_prompt: Union[str, None] = None,
        stable_settings_negative_prompt: Union[str, None] = None,
):
    if "--no " in eng_text:
        positive, negative = eng_text.split("--no ", 1)
    else:
        positive = eng_text
        negative = ""
    if style_positive_prompt or style_negative_prompt:
        positive_prompt = style_positive_prompt.format(prompt=positive)
        negative_prompt = f"{negative} {style_negative_prompt}"
    elif custom_settings_positive_prompt or custom_settings_negative_prompt:
        positive_prompt = custom_settings_positive_prompt.format(prompt=positive)
        negative_prompt = f"{negative} {custom_settings_negative_prompt}"
    else:
        positive_prompt = f"{positive} {stable_settings_positive_prompt}"
        negative_prompt = f"{negative} {stable_settings_negative_prompt}"
    return positive_prompt, negative_prompt


async def get_stable_data(
        message: StableMessage,
        user: User,
        stable_settings: StableSettings,
        session: AsyncSession,
        main_callback_url: bool = False
) -> dict:
    eng_text = message.eng_text

    custom_settings = user.custom_settings
    style = user.style
    model_id = stable_settings.model_id or "flux"
    num_inference_steps = stable_settings.num_inference_steps or "31"
    guidance_scale = stable_settings.guidance_scale or 7
    sampling_method = stable_settings.sampling_method or ""
    algorithm_type = stable_settings.algorithm_type or ""
    scheduler = stable_settings.scheduler or ""
    embeddings_models = stable_settings.embeddings_model or None
    lora_model = stable_settings.lora_model
    lora_strength = stable_settings.lora_strength
    if custom_settings:
        model_id = custom_settings.model_id or model_id
        num_inference_steps = custom_settings.num_inference_steps or num_inference_steps
        guidance_scale = custom_settings.guidance_scale or guidance_scale
        sampling_method = custom_settings.sampling_method or sampling_method
        algorithm_type = custom_settings.algorithm_type
        scheduler = custom_settings.scheduler or scheduler
        embeddings_models = custom_settings.embeddings_model or embeddings_models
        lora_model = custom_settings.lora_model or lora_model
        lora_strength = custom_settings.lora_strength or lora_strength

    scale = ""
    if "--ar " in eng_text:
        scale = eng_text.split("--ar ")[-1]
    width, height = get_sizes(scale)
    seed = randint(0, 16000000)
    await _update_message(
        message.id,
        {"width": width, "height": height, "seed": str(seed)},
        session
    )
    positive_prompt, negative_prompt = get_user_prompts(
        eng_text=eng_text,
        style_positive_prompt=style.positive_prompt if style else None,
        style_negative_prompt=style.negative_prompt if style else None,
        custom_settings_positive_prompt=custom_settings.positive_prompt if custom_settings else None,
        custom_settings_negative_prompt=custom_settings.negative_prompt if custom_settings else None,
        stable_settings_positive_prompt=stable_settings.positive_prompt if stable_settings else None,
        stable_settings_negative_prompt=stable_settings.negative_prompt if stable_settings else None,
    )
    callback_url = "/async/stable/stable_webhook/"
    if main_callback_url:
        callback_url = "/stable/stable_webhook/"
    data = {
        "key": STABLE_API_KEY,
        "model_id": model_id,
        "prompt": positive_prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "samples": 4,
        "num_inference_steps": num_inference_steps,
        "seed": str(seed),
        "guidance_scale": guidance_scale,
        "enhance_prompt": "no",
        "safety_checker": "no",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "yes",
        "upscale": "no",
        "lora_model": lora_model,
        "lora_strength": lora_strength,
        "sampling_method": sampling_method,
        "instant_response": True,
        "algorithm_type": algorithm_type,
        "scheduler": scheduler,
        # "embeddings_model": "vae-for-human" or embeddings_models,
        "webhook": SITE_DOMAIN + callback_url,
        "track_id": message.id,
        "tomesd": "yes",
        "use_karras_sigmas": "yes",
        "vae": None,
    }
    return data


async def handle_stable_text2img_answer(
        response_data: dict,
        message: StableMessage,
        remain_messages: int,
        session: AsyncSession,
):
    if response_data.get("status") in ["success", "processing"]:
        message_data = {"stable_request_id": str(response_data.get("id"))}
        single_images = response_data.get("future_links")
        try:
            message_data["first_image"] = single_images[0]
            message_data["second_image"] = single_images[1]
            message_data["third_image"] = single_images[2]
            message_data["fourth_image"] = single_images[3]
        except Exception:
            print("no images")
    else:
        await _update_user(message.user_id, {"remain_messages": remain_messages}, session)
        message_data = {"answer_sent": True}
        await bot_send_text_message(
            telegram_chat_id=message.telegram_chat_id,
            text=f"<pre>Генерация по запросу '{message.initial_text}' не удалась. Попробуйте снова</pre>"
        )
    message_data["sent_to_stable"] = True
    await _update_message(message.id, update_data=message_data, session=session)


async def handle_stable_upscale_answer(
        response_data: dict,
        message: StableMessage,
        remain_messages: int,
        session: AsyncSession
):
    status = response_data.get("status")
    request_id = str(response_data.get("id"))
    if status == "success":
        message_data = {
            "stable_request_id": request_id,
            "single_image": response_data.get("output")[0],
        }
    elif status == "processing":
        message_data = {
            "stable_request_id": request_id,
        }
    else:
        await _update_user(message.user_id, {"remain_messages": remain_messages}, session)
        message_data = {"answer_sent": True}
        await bot_send_text_message(
            telegram_chat_id=message.telegram_chat_id,
            text=f"<pre>Генерация по запросу '{message.initial_text}' не удалась. Попробуйте снова</pre>"
        )
    message_data["sent_to_stable"] = True
    await _update_message(message.id, update_data=message_data, session=session)


async def handle_stable_fetch_answer(
        response_data: dict,
        message: StableMessage,
        remain_messages: int,
        session: AsyncSession,
) -> Union[StableMessage | None]:
    status = response_data.get("status")
    if status == "success":
        images = response_data.get("output")
        message_data = {
            "first_image": images[0],
            "second_image": images[1],
            "third_image": images[2],
            "fourth_image": images[3],
        }
        return await _update_message(message.id, update_data=message_data, session=session)
    elif status in ["failed", "error"]:
        await _update_user(message.user_id, {"remain_messages": remain_messages}, session)
        await _update_message(message.id, update_data={"answer_sent": True}, session=session)
        await bot_send_text_message(
            telegram_chat_id=message.telegram_chat_id,
            text=f"Генерация по запросу '{message.initial_text}'"
                 " не удалась. Вам добавлена одна генерация. Попробуйте снова"
        )


async def check_remains(
        eng_text: str,
        user: User,
        chat_id: int,
        session: AsyncSession
):
    if not eng_text.startswith("button_u&&"):
        if user.remain_messages == 0:

            if not user.date_of_payment or user.date_payment_expired.replace(tzinfo=None) < datetime.now():
                await bot_send_text_message(
                    telegram_chat_id=chat_id,
                    text="Пожалуйста, оплатите доступ к боту"
                )
                return False
        if user.remain_paid_messages > 0 and user.date_payment_expired.replace(tzinfo=None) >= datetime.now():
            remain_paid_messages = user.remain_paid_messages - 1
            await _update_user(user.id, {"remain_paid_messages": remain_paid_messages}, session)
        elif user.remain_messages > 0:
            remain_messages = user.remain_messages - 1
            await _update_user(user.id, {"remain_messages": remain_messages}, session)
        else:
            await bot_send_text_message(
                telegram_chat_id=chat_id,
                text="У вас не осталось генераций",
            )
            return False
    return True
