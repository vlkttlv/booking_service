from pydantic import BaseModel, EmailStr

class SUserAuth(BaseModel): # схемы нужны для валидации данных
    email: EmailStr
    password: str