from telegram_message import button_message


async def test_set_style(client, create_user_in_database, get_user_from_database):
    request_json = button_message
    request_json["callback_query"]["data"] = "style&&new_style"
    request_json["callback_query"]["from"]["username"] = "set_style_user"

    await create_user_in_database("set_style_user")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при установке стиля"

    user = await get_user_from_database("set_style_user")
    assert user, "Не создался нужный пользователь"
    assert user[0].style.name == "new_style", "Некорректно установился стиль"

    request_json["callback_query"]["data"] = "style&&info"

    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при запросе стиля"

    user = await get_user_from_database("set_style_user")
    assert user[0].style.name == "new_style", "Изменился стиль"

    request_json["callback_query"]["data"] = "style&&del"

    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при запросе стиля"

    user = await get_user_from_database("set_style_user")
    assert not user[0].style, "Не удалился стиль"


async def test_set_format(client, create_user_in_database, get_user_from_database):
    request_json = button_message
    request_json["callback_query"]["data"] = "preset&& --ar 3:2"
    request_json["callback_query"]["from"]["username"] = "set_format_user"

    await create_user_in_database("set_format_user")
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при установке формата"

    user = await get_user_from_database("set_format_user")
    assert user, "Не создался нужный пользователь"
    assert user[0].preset == " --ar 3:2", "Некорректно установился формат"

    request_json["callback_query"]["data"] = "preset&&info"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при запросе формата"

    user = await get_user_from_database("set_format_user")
    assert user[0].preset == " --ar 3:2", "Формат изменился"

    request_json["callback_query"]["data"] = "preset&&del"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200, "Неверный статус при удалении формата"

    user = await get_user_from_database("set_format_user")
    assert not user[0].preset, "Формат не удалился"
