import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize("id,exists,email", [
    (1, True, 'test@test.com'),
    (2, True, 'user@user.com'),
    (20, False, 'email@tpu.com')
])  # создаем несколько тестовых случаев с различными данными
async def test_find_user_by_id(id, exists, email):
    user = await UsersDAO.find_by_id(id)
    if exists:
        assert user
        assert user.email == email
        assert user.id == id
    else:
        assert not user
