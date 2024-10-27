from datetime import datetime
from fastapi import Depends, Request
from jose import JWTError
import jwt

from app.config import settings
from app.exceptions import IncorrectTokenFormatException
from app.users.dao import UsersDAO


def get_token(request: Request):
    """Метод, получающий текущий токен"""
    token = request.cookies.get("booking_access_token")
    if not token:
        return "not_token"
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Возвращает пользователя (при необходимости его данные можно получить)"""
    if token == "not_token":
        return "user"
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError as e:
        return "user"
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        return "user"
    user_id: str = payload.get("sub")
    if not user_id:
        return "user"
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        return "user"
    return user.role
