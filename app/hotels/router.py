import ast
from datetime import date, datetime
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from app.hotels.models import Hotels
from app.hotels.rooms.dao import RoomDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import IncorrectRoleException, WrongDateFrom
from app.hotels.dao import HotelDAO, HotelImagesDAO
from app.hotels.schemas import SHotelAdd, SHotelInfo, SHotels

import pandas as pd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
# @cache(expire=20)
async def get_hotels(
    location: str,
    date_from: date = Query(..., description=f"Например, {
                            datetime.now().date()}"),
    date_to: date = Query(
        ...,
        description=f"Например, {
            datetime.now().date()}",
    ),
    services: str = Query(
        "Парковка", description="Вводите услуги через пробел"
    ),
    min_check: int = 0,
    max_check: int = 100_000,
) -> List[SHotelInfo]:
    """Получение всех отелей для указанной локации, дат и ценового диапазона."""
    if date_from >= date_to:
        raise WrongDateFrom
    return await HotelDAO.find_all_by_location_and_date(
        location, date_from, date_to, services, min_check, max_check
    )


@router.post("/add_hotel")
async def add_hotel(hotel_data: SHotelAdd, user: Users = Depends(get_current_user)):
    """Добавление отеля. Доступно только администраторам"""
    if user.role != "admin":
        raise IncorrectRoleException
    new_hotel_id = await HotelDAO.add(
        name=hotel_data.name,
        location=hotel_data.location,
        services=hotel_data.services,
        rooms_quantity=hotel_data.rooms_quantity,
    )
    for i in range(1, 4):
        await HotelImagesDAO.add(hotel_id=new_hotel_id, image_id=i)


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


@router.post("/add_hotels_and_rooms_in_db")
async def add_hotels_and_rooms_in_db():

    with open("hotels.json", 'r') as file:
        hotels_data = json.load(file)  # Загружаем данные из JSON

        for hotel in hotels_data:

            await HotelDAO.add(name=hotel['name'],
                               location=hotel['location'],
                               services=hotel['services'],
                               rooms_quantity=hotel['rooms_quantity'])
    with open("rooms.json", 'r') as file:
        rooms_data = json.load(file)  # Загружаем данные из JSON

        for room in rooms_data:

            await RoomDAO.add(hotel_id=room['hotel_id'],
                              name=room['name'],
                              description=room['description'],
                              price=room['price'],
                              services=room['services'],
                              quantity=room['quantity'])

    return {"detail": 'отели и комнаты были добавлены в БД'}
