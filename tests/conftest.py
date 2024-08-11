import asyncio
from typing import AsyncGenerator, Generator, Any

import asyncpg
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from sqlalchemy import insert, text, select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database_interaction import metadata, get_db
from main import app
from schemas import User
from schemas.site_settings import SiteSettings
from settings import TEST_DATABASE_URL

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test
pytest_plugins = ('pytest_asyncio',)

CLEAN_TABLES = [
    "bot_config_sitesettings",
    "users_user"
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session", autouse=True)
# async def run_migrations():
#     os.system("alembic init migrations")
#     os.system('alembic revision --autogenerate -m "test running migrations"')
#     os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="session", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture(scope="session", autouse=True)
async def create_site_settings(async_session_test):
    """Creating site settings row"""
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(
                insert(SiteSettings).values(
                    {
                        "day_tariff_cost": 300,
                        "month_tariff_cost": 1000,
                        "day_tariff_count": 300,
                        "month_tariff_count": 1000,
                        "say_hi_video": None,
                        "say_hi_video_video_bot": None,
                        "notice_message": None,
                        "settings_lesson_link": "https://ya.ru",
                        "queue_number": 1
                    }
                )
            )


@pytest.fixture(scope="session")
async def create_user_in_database(async_session_test):
    """Creating user"""

    async def create_user_in_database_by_username(username: str):
        async with async_session_test() as session:
            await session.execute(
                insert(User).values(
                    {
                        "username": username,
                        "password": "12345",
                        "remain_messages": 10,
                        "is_active": True,
                    }
                )
            )
            await session.commit()
    return create_user_in_database_by_username


@pytest.fixture
async def get_user_from_database(async_session_test):
    async def get_user_from_database_by_username(username: str):
        async with async_session_test() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return list(result.scalars())

    return get_user_from_database_by_username


@pytest.fixture
async def set_generations_to_user(async_session_test):
    async def set_generations_to_user_by_username(username: str):
        async with async_session_test() as session:
            result = await session.execute(
                update(User).where(User.username == username).values({"remain_messages": 10})
            )
            return list(result.scalars())

    return set_generations_to_user_by_username
