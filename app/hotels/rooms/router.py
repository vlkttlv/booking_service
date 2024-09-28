from datetime import date
from fastapi import APIRouter, Depends

from app.exceptions import IncorrectRoleException
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomAdd
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomDAO.find_all_rooms(hotel_id, date_from, date_to)


@router.post("/{hotel_id}/add_room")
async def add_hotel(room_data: SRoomAdd, user: Users = Depends(get_current_user)):
    if user.role != 'admin':
        raise IncorrectRoleException
    return await RoomDAO.add(hotel_id=room_data.hotel_id, name=room_data.name, description=room_data.description,
                             services=room_data.services, quantity=room_data.rooms_quantity, price=room_data.price, image_id=room_data.image_id)
