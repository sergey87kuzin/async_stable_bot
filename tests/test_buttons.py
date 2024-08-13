from telegram_message import button_message


async def test_set_commands(client, create_user_in_database):
    request_json = button_message
    request_json["callback_query"]["data"] = "style&&new_style"
    request_json["callback_query"]["from"]["username"] = "set_commands_user"

    await create_user_in_database("set_commands_user")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при установке стиля"
