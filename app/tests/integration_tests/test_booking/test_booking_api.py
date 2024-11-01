from datetime import datetime
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (1, "2025-08-10", "2025-09-01", 3, 200),
    (1, "2025-08-10", "2025-09-01", 4, 200),
    (1, "2025-08-10", "2025-09-01", 5, 200),
    (1, "2025-08-10", "2025-09-01", 5, 409),
    # 2 брони уже есть, еще 3 добавятся, 5я уже нет (всего 5 комнат)

])
async def test_add_and_get_booking(auth_ac: AsyncClient, room_id, date_from, date_to, status_code, booked_rooms):
    response = await auth_ac.post("/v1/bookings", params={"room_id": room_id,
                                                          "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
                                                          "date_to": datetime.strptime(date_to, "%Y-%m-%d")})

    assert response.status_code == status_code
    response = await auth_ac.get('/v1/bookings')
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_bookings(auth_ac: AsyncClient):
    response = await auth_ac.get('/v1/bookings')
    # получаем все айди броней в виде списка
    all_bookings = [booking['id'] for booking in response.json()]
    for booking_id in all_bookings:  # проходимся по каждому бронированию и удаляем его
        response = await auth_ac.delete(
            f"/v1/bookings/{booking_id}",
        )
    response = await auth_ac.get("/v1/bookings")
    assert len(response.json()) == 0  # проверка, что у 1 юзера 0 броней
