from app.booking.dao import BookingDAO
from datetime import datetime
from app.booking.models import Bookings


async def test_add_and_get_and_delete_booking():
    new_booking = await BookingDAO.add(user_id=2,
                                       room_id=4,
                                       date_from=datetime.strptime(
                                           "2025-08-10", "%Y-%m-%d"),
                                       date_to=datetime.strptime("2025-09-01", "%Y-%m-%d"))
    assert new_booking.user_id == 2
    assert new_booking.room_id == 4
    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None
    await BookingDAO.delete(id=new_booking.id, user_id=2)
    response = await BookingDAO.find_by_id(new_booking.id)
    assert response is None
