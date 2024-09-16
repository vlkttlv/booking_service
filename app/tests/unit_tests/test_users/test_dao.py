from app.users.dao import UsersDAO
import pytest


@pytest.mark.parametrize("id,exists,email", [
    (1, True, 'test@test.com'),
    (2, True, 'vvb63@tpu.ru'),
    (5, False, 'email')
])
async def test_find_user_by_id(id, exists, email):
    user = await UsersDAO.find_by_id(id)
    if exists:
        assert user
        assert user.email == email
        assert user.id == id
    else:
        assert not user
