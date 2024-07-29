import asyncio
from datetime import date
from typing import List, Optional
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelInfo, SHotels
from fastapi_cache.decorator import cache
router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/{location}")
@cache(expire=20)
async def get_hotels(location: str, date_from: date, date_to: date) -> List[SHotelInfo]:
    return await HotelDAO.find_all_by_location_and_date(location, date_from, date_to)


@router.get("/id/{hotel_id}", include_in_schema=True)
# Этот эндпоинт используется для фронтенда, когда мы хотим отобразить все
# номера в отеле и информацию о самом отеле. Этот эндпоинт как раз отвечает за информацию
# об отеле.
# В нем нарушается правило именования эндпоинтов: конечно же, /id/ здесь избыточен.
# Тем не менее, он используется, так как эндпоинтом ранее мы уже задали получение
# отелей по их локации вместо id.
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotels]:
    return await HotelDAO.find_one_or_none(id=hotel_id)