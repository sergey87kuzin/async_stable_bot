import pytest

from telegram_message import text_message


async def test_text_message(
        client,
        create_user_in_database,
        set_user_free_generations,
        set_user_generations_wrong_date,
        set_user_generations_right_date
):
    request_json = text_message
    request_json["text"] = "some interesting prompt"
    request_json["chat"]["username"] = "SomeUser"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 204, "Неверный статус при несозданном пользователе"

    await create_user_in_database("SomeUser")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 204, "Неверный статус при недостатке генераций"

    await set_user_generations_wrong_date("SomeUser")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 204, "Неверный статус при истекшей дате генераций"

    await set_user_generations_right_date("SomeUser")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при корректной дате генераций"

    await set_user_free_generations("SomeUser")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при достаточном числе генераций"
