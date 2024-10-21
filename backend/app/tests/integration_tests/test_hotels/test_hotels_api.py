from datetime import datetime
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ('Алтай', '2025-06-01', '2025-06-11', 200),
    ('Алтай', '2025-06-01', '2025-06-01', 200),
    ('Алтай', '2025-06-11', '2025-06-01', 400),
])
async def test_get_hotels(auth_ac: AsyncClient, location, date_from, date_to, status_code):
    response = await auth_ac.get(f"/hotels/{location}", params={"location": location,
                                                                "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
                                                                "date_to": datetime.strptime(date_to, "%Y-%m-%d"),
                                                                "min_check": 0,
                                                                "max_check": 100000,
                                                                "service": 'Парковка'})

    assert response.status_code == status_code
