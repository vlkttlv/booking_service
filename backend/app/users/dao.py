from backend.app.dao.base import BaseDAO
from backend.app.users.models import Users


class UsersDAO(BaseDAO):
    """Класс для работы с БД. Наследуется от базового класса"""
    model = Users
