from datetime import datetime
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("location,date_from,date_to,min_check,max_check,services,status_code,hotels", [
    ('Алтай', '2024-11-01', '2024-11-11', 0, 100000, 'Парковка', 200, 3),
    ('Алтай', '2024-11-01', '2025-11-01', 0, 5000, 'Парковка', 200, 1),
    ('Алтай', '2024-11-01', '2024-11-11', 0, 100000, 'Бассейн Парковка', 200, 1),
    ('Алтай', '2024-11-21', '2024-11-01', 0, 100000, 'Парковка', 400, 1),
])
async def test_get_hotels(auth_ac: AsyncClient, location, date_from, date_to, min_check, max_check, services, status_code, hotels):
    response = await auth_ac.get(f"/v1/hotels/{location}", params={"location": location,
                                                                   "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
                                                                   "date_to": datetime.strptime(date_to, "%Y-%m-%d"),
                                                                   "min_check": min_check,
                                                                   "max_check": max_check,
                                                                   "services": services})

    assert response.status_code == status_code
    assert len(response.json()) == hotels
