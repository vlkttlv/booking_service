from datetime import date
from fastapi import APIRouter, Depends

from backend.app.exceptions import IncorrectRoleException
from backend.app.hotels.rooms.dao import RoomDAO, RoomImagesDAO
from backend.app.hotels.rooms.schemas import SRoomAdd
from backend.app.users.dependencies import get_current_user
from backend.app.users.models import Users


router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomDAO.find_all_rooms(hotel_id, date_from, date_to)


@router.post("/{hotel_id}/add_room")
async def add_room(room_data: SRoomAdd, user: Users = Depends(get_current_user)):
    if user.role != 'admin':
        raise IncorrectRoleException
    new_room_id = await RoomDAO.add(hotel_id=room_data.hotel_id, name=room_data.name, discription=room_data.description,
                                    sevices=room_data.services, quantity=room_data.quantity, price=room_data.price)
    for i in range(1, 4):
        await RoomImagesDAO.add(room_id=new_room_id, image_id=i)
