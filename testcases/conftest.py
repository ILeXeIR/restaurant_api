import asyncio
import pytest
import uuid

from databases import Database
from httpx import AsyncClient
from sqlalchemy import MetaData, create_engine

from main import app
from src.menu.models import menus


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", name="ac")
async def create_async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture(scope="session")
async def create_test_db():
    test_db_url = "postgresql://postgres:postgres@test_db:5432/postgres_db"
    database = Database(test_db_url)
    metadata = MetaData()
    engine = create_engine(test_db_url)
    metadata.create_all(engine)
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture()
async def db_with_menus(create_test_db):
    db = create_test_db
    test_menus = [
        {
            "id": str(uuid.uuid4()),
            "title": "Test menu 1",
            "description": "Test menu description 1"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Test menu 2",
            "description": "Test menu description 2"
        }
    ]
    for test_menu in test_menus:
        query = menus.insert().values(**test_menu)
        await db.execute(query)
    yield
    query = menus.delete()
    await db.execute(query)
