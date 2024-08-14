import pytest

from periodic_tasks import check_not_sent_to_telegram


@pytest.mark.parametrize("username", [
    "first_user",
    "second_user",
])
async def test_send_to_telegram(create_user_in_database, create_message_in_database, async_session_test, username):
    user = await create_user_in_database(username)
    message = await create_message_in_database(user)
    async with async_session_test() as session:
        await check_not_sent_to_telegram({"db_session": session})
