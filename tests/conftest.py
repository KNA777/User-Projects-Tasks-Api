import pytest
from httpx import AsyncClient, ASGITransport
from src.api.dependencies import get_db
from src.context_manager_db.context_manager import DBManager
from src.main import app
from src.models import *
from src.db_config import engine_null_pool, BaseOrm, async_session_null_pool
from src.schemas.users import UserRegRequest
from src.services.auth import AuthService
from src.settings_config import settings


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def db_null_pool():  # -> DBManager
    async with DBManager(session_factory=async_session_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in db_null_pool():
        yield db


app.dependency_overrides[get_db] = db_null_pool  # перезаписываем для тестирования API, чтобы db был c null pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as connect:
        await connect.run_sync(BaseOrm.metadata.drop_all)
        await connect.run_sync(BaseOrm.metadata.create_all)

    async with DBManager(session_factory=async_session_null_pool) as db_:
        user = UserRegRequest(
            username="nikita",
            email="ya@ya.ru",
            password="12345678",
            is_superuser=False,
        )
        await AuthService(db_).registration(user)


@pytest.fixture(scope="session")
async def ac(setup_database):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac):
    await ac.post(
        "/auth/registration",
        json={
            "username": "kot",
            "email": "kot@pess.com",
            "password": "12345678",
            "is_superuser": True
        })


@pytest.fixture(scope="session")
async def auth_ac(ac, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pess.com",
            "password": "12345678",
        }
    )
    user = await ac.get(
        url="/users/get_me",
    )
    print(user.json())
    assert ac.cookies["access_token"]
    yield {"ac_client": ac, "user": user.json()}


@pytest.fixture(scope="session", autouse=True)
async def add_project(auth_ac):
    await auth_ac["ac_client"].post(
        url="/projects",
        json={
            "name": "name",
            "description": "description",
        })
