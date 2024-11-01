"""hhtpx предоставляет асинхронного клиента для тестов"""
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("example@gmail.com", "sobaka2000", 201),
    ("example@gmail.com", "qwerty", 409),
    ("mock@mock.com", "qwerty", 201),
    ("ne_email", "qwerty", 422)])
async def test_register_user(ac: AsyncClient, email,
                             password, status_code):
    """Тест, проверяющий регистрацию пользователя"""
    response = await ac.post("/v1/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("test@test.com", "wrong_test", 401),
    ("fake@test.com", "password", 401)
])
async def test_login_user(ac: AsyncClient, email, password, status_code):
    """Тест, проверяющий вход пользователя в систему"""
    response = await ac.post("/v1/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
