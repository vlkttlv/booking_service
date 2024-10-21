from typing import Optional
from pydantic import BaseModel
from datetime import date

from sqlalchemy import JSON


class SBooking(BaseModel):  # схемы нужны для валидации данных

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        from_attributes = True


class SBookingInfo(SBooking):
    image_id: int
    name: str
    description: Optional[str]
    services: list[str]

    class Config:
        orm_mode = True


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
