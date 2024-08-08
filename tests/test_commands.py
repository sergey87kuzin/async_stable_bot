import pytest

from telegram_message import text_message

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_start_command(client, get_user_from_database):
    request_json = text_message
    request_json["text"] = "/start"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Запрос на старт чата дает неправильный статус"
    users = await get_user_from_database("SergeyAKuzin")
    assert len(users) == 1, "Должен быть создан только один пользователь"


@pytest.mark.asyncio
async def test_menu_command(client):
    request_json = text_message
    request_json["text"] = "/instruction"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Запрос команды инструкции дает неправильный статус"
