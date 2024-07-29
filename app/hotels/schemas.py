from typing import List
from pydantic import BaseModel
from sqlalchemy import JSON
from app.database import Base

class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int
    rooms_quantity: int 

class SHotelInfo(SHotels):
    free_rooms: int

    class Config:
        from_attributes = True