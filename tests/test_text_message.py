import pytest

from telegram_message import text_message


async def test_text_message(client, create_user_in_database):
    request_json = text_message
    request_json["text"] = "some interesting prompt"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 204, "Неверный статус при недостаточном числе генераций"

    await create_user_in_database("SergeyAKuzin")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при достаточном числе генераций"
