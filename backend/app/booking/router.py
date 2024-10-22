from datetime import date
from fastapi import APIRouter, Depends, Request
from pydantic import parse_obj_as
from sqlalchemy import delete, select
from fastapi_versioning import version
from backend.app.booking.dao import BookingDAO
from backend.app.database import async_session_maker
from backend.app.booking.models import Bookings
from backend.app.booking.schemas import SBooking
from backend.app.exceptions import RoomCannotBeBooked
from backend.app.tasks.tasks import send_booking_confirmation_email
from backend.app.users.dependencies import get_current_user
from backend.app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
@version(1)  # определяем версию
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    """Получение всех бронирований пользователя"""
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: Users = Depends(get_current_user)):
    """Добавление бронирование"""
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)


@router.delete("/{booking_id}",  status_code=204)
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    """Удаление брони"""
    await BookingDAO.delete(user_id=user.id, id=booking_id)
