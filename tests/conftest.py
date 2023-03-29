import asyncio
import os
import sys

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from base.settings import settings
from base.database import Base, get_session
from main import app


class TestDB:
    DB_NAME = os.getenv("TEST_DB_NAME")
    DB_USER = os.getenv("TEST_DB_USER")
    DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
    TEST_DSN = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{DB_NAME}"

    def __init__(self):
        self.engine = create_async_engine(settings.database_dsn, future=True, isolation_level="AUTOCOMMIT")

    async def create(self) -> create_async_engine:
        async with self.engine.connect() as conn:
            await conn.execute(text(f"DROP DATABASE IF EXISTS {self.DB_NAME}"))
            await conn.execute(text(f"DROP USER IF EXISTS {self.DB_USER}"))
            await conn.execute(text(f"CREATE DATABASE {self.DB_NAME}"))
            await conn.execute(text(f"CREATE USER {self.DB_USER} WITH PASSWORD '{self.DB_PASSWORD}'"))
            await conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE {self.DB_NAME} TO {self.DB_USER}"))
            await conn.execute(text(f"ALTER USER {self.DB_USER} WITH SUPERUSER"))
        return create_async_engine(self.TEST_DSN, future=True)

    async def drop(self):
        async with self.engine.connect() as conn:
            await conn.execute(text(f"DROP DATABASE {self.DB_NAME}"))
            await conn.execute(text(f"DROP USER {self.DB_USER}"))
        await self.engine.dispose()


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine(event_loop) -> AsyncEngine:
    test_db = TestDB()
    test_engine = await test_db.create()
    yield test_engine
    await test_engine.dispose()
    await test_db.drop()


@pytest.fixture(scope="function")
async def sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_sessionmaker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield test_sessionmaker

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session(sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        yield session


@pytest.fixture(scope="function")
async def fastapi_app(sessionmaker: async_sessionmaker):
    async def get_test_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield app


@pytest.fixture(scope="function")
async def client(fastapi_app):
    async with AsyncClient(app=fastapi_app, base_url=settings.server_address) as client:
        yield client
