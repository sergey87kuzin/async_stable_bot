import pytest

from telegram_message import text_message


@pytest.mark.asyncio
async def test_text_message(client, get_user_from_database):
    request_json = text_message
    request_json["text"] = "some interesting prompt"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 204, "Запрос на старт чата дает неправильный статус"
