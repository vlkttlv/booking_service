"""hhtpx предоставляет асинхронного клиента для тестов"""
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("sobaka@pes.com", "sobaka2000", 200),
    ("sobaka@pes.com", "qwerty", 409),
    ("pes@pes.com", "qwerty", 200),
    ("ne_email", "qwerty", 422)])
async def test_register_user(ac: AsyncClient, email,
                             password, status_code):
    """Тест, проверяющий регистрацию пользователя"""
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("test@test.com", "fake_test", 401),
    ("fake@people.com", "pass", 401)
])
async def test_login_user(ac: AsyncClient, email, password, status_code):
    """Тест, проверяющий вход пользователя в систему"""
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
