import pytest

from telegram_message import text_message

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_start_command(client):
    request_json = text_message
    request_json["text"] = "/start"
    response = client.post('/telegram', json=request_json)

    assert response.status_code == 200
