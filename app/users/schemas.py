from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):  # схемы нужны для валидации данных
    """Схема для аутенфикации пользователя"""
    email: EmailStr
    password: str
