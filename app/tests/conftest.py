import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.database import Base, async_session_maker, engine
from app.config import settings

from app.booking.models import Bookings
from app.users.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.payments.models import Payments

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app as fastapi_app
# фикстура - функция, котор-я подготавливает среду для тестирования


@pytest.fixture(autouse=True, scope="session")
# подъем БД
# наполнение БД таблицами, а таблиц данным
# часто переиспользуемые данные, можно возвращать через фикстуру
# отдают через ключеове слово yeild сессии
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_test_json(model: str):
        with open(f"app/tests/test_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_test_json("hotels")
    rooms = open_test_json("rooms")
    users = open_test_json("users")
    bookings = open_test_json("bookings")
    payments = open_test_json("payments")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(
            booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    for payment in payments:
        payment["date_to"] = datetime.strptime(payment["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)
        add_payments = insert(Payments).values(payments)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)
        await session.execute(add_payments)

        await session.commit()

# Взято из документации pytest-asyncio


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("v1/auth/login", json={"email": "test@test.com", "password": "test"})
        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
