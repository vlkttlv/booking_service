from app.booking.dao import BookingDAO
from datetime import datetime
from app.booking.models import Bookings


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(user_id=2,
                                       room_id=4,
                                       date_from=datetime.strptime(
                                           "2025-08-10", "%Y-%m-%d"),
                                       # добавляем бронирование с помощью метода
                                       date_to=datetime.strptime("2025-09-01", "%Y-%m-%d"))
    assert new_booking.user_id == 2
    assert new_booking.room_id == 4
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None
    await BookingDAO.delete(id=new_booking.id, user_id=2)
    response = await BookingDAO.find_by_id(new_booking.id)
    assert response is None
    """

Добавление брони (данная операция возвращает id добавленной записи)
Чтение брони (используя полученный id)
Удаление брони
Чтение брони (необходимо убедиться, что бронь удалилась"""


async def test_delete_booking():
    ...


async def test_read_booking():
    ...
