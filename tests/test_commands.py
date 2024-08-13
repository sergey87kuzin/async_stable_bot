import pytest

from telegram_message import text_message

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_start_command(client, get_user_from_database):
    request_json = text_message
    request_json["text"] = "/start"
    request_json["chat"]["username"] = "SergeyAKuzin"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Запрос на старт чата дает неправильный статус"
    users = await get_user_from_database("SergeyAKuzin")
    assert len(users) == 1, "Должен быть создан только один пользователь"


@pytest.mark.parametrize(
    "command,status,error_text", [
        ("/instruction", 200, "Запрос на инструкцию дает неверный статус"),
        ("/lessons", 200, "Запрос на уроки дает неверный статус"),
        ("/style", 200, "Запрос на стили дает неверный статус"),
        ("/format", 200, "Запрос на форматы дает неверный статус"),
        ("/authorization", 200, "Запрос на авторизацию дает неверный статус"),
        ("/password", 204, "Запрос на смену пароля дает неверный статус"),
        ("/password 12345", 200, "Запрос на смену пароля дает неверный статус"),
        ("/payment", 200, "Запрос на оплату дает неверный статус"),
        ("/support", 200, "Запрос на поддержку дает неверный статус"),
        ("/information", 200, "Запрос на инфо дает неверный статус"),
        ("/mybot", 200, "Запрос мой бот дает неверный статус"),
        ("/help", 200, "Запрос на помощь дает неверный статус"),
        ("/other_command", 204, "Запрос с неправильной командой дает неверный статус")
    ]
)
async def test_menu_command(client, command, status, error_text):
    request_json = text_message
    request_json["text"] = command
    response = client.post('/telegram', json=request_json)

    assert response.status_code == status, error_text
