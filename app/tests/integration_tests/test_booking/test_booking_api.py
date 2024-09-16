from datetime import datetime
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (10, "2025-08-10", "2025-09-01", 3, 200),
    (10, "2025-08-10", "2025-09-01", 4, 200),
    (10, "2025-08-10", "2025-09-01", 5, 200),
    (10, "2025-08-10", "2025-09-01", 6, 200),
    (10, "2025-08-10", "2025-09-01", 7, 200),
    (10, "2025-08-10", "2025-09-01", 8, 200),
    (10, "2025-08-10", "2025-09-01", 9, 200),
    (10, "2025-08-10", "2025-09-01", 9, 409),

])
async def test_add_and_get_booking(auth_ac: AsyncClient, room_id, date_from, date_to, status_code, booked_rooms):
    response = await auth_ac.post("/bookings", params={"room_id": room_id,
                                                       "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
                                                       "date_to": datetime.strptime(date_to, "%Y-%m-%d")})

    assert response.status_code == status_code
    response = await auth_ac.get('/bookings')
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(auth_ac: AsyncClient):
    response = await auth_ac.get('/bookings')
    all_bookings = [booking['id'] for booking in response.json()]
    for booking_id in all_bookings:
        response = await auth_ac.delete(
            f"/bookings/{booking_id}",
        )

    response = await auth_ac.get("/bookings")
    assert len(response.json()) == 0
