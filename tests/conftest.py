import asyncio
from typing import AsyncGenerator, Generator, Any

import asyncpg
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database_interaction import metadata, get_db
from main import app
from schemas.site_settings import SiteSettings
from settings import TEST_DATABASE_URL

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def create_sitesettings(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(
                """INSERT INTO bot_config_sitesettings VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);""",
                1,
                300,
                1000,
                None,
                200,
                1000,
                None,
                None,
                "https://ya.ru",
                1
            )


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


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
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


# @pytest.fixture
# async def create_site_settings_in_database(asyncpg_pool):
#     async def create_site_settings_in_database():
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.execute(
#                 """INSERT INTO bot_config_sitesettings VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);""",
#                 1,
#                 300,
#                 1000,
#                 None,
#                 200,
#                 1000,
#                 None,
#                 None,
#                 "https://ya.ru",
#                 1
#             )
#
#     return create_site_settings_in_database
