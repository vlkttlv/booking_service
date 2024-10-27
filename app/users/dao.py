from app.dao.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    """Класс для работы с БД. Наследуется от базового класса"""
    model = Users
