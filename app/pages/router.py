from datetime import date, datetime
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.router import get_rooms
from app.hotels.router import get_hotel_by_id, get_hotels
from app.booking.router import get_bookings
from app.users.dependencies import get_role_of_current_user
from app.hotels.models import Hotels
from app.config import settings

router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/main", response_class=HTMLResponse)
async def get_hotels_pages(request: Request):
    return templates.TemplateResponse(name="main.html", context={"request": request})


@router.get("/auth/register")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@router.get("/auth/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(request: Request, location: str, date_from: date, date_to: date, min_check: int,
                          max_check: int, services: str,
                          hotels=Depends(get_hotels),
                          ):
    return templates.TemplateResponse(
        "hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "min_check": min_check,
            "max_check": max_check,
            "services": services,
        },
    )


@router.get("/rooms")
async def get_rooms_pages(request: Request, date_from: date, date_to: date,
                          rooms=Depends(get_rooms), hotel=Depends(get_hotel_by_id),):
    booking_date = (date_to - date_from).days
    return templates.TemplateResponse(name="rooms.html", context={"request": request, "rooms": rooms, "hotel": hotel,
                                                                  "booking_date": booking_date, "date_from": date_from,
                                                                  "date_to": date_to})


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(request: Request, bookings=Depends(get_bookings)):
    return templates.TemplateResponse("bookings.html", {"request": request, "bookings": bookings})


@router.get("/payments/pay")
async def pay(request: Request, booking_id: int, stripe_key: str = settings.STRIPE_PUBLISHABLE_KEY):
    return templates.TemplateResponse(name="pay.html", context={"request": request, "booking_id": booking_id, "stripe_key": stripe_key})


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse(name="login-admin.html", context={"request": request})


@router.get("/admin/main")
async def admin_main(request: Request, role_of_current_user=Depends(get_role_of_current_user)):
    return templates.TemplateResponse(name="main-admin.html", context={"request": request})


@router.get("/admin/hotels/list")
async def get_hotels_list(request: Request, role_of_current_user=Depends(get_role_of_current_user)):
    hotels = await HotelDAO.find_all()
    return templates.TemplateResponse(name="hotels-admin.html", context={"request": request, "hotels": hotels})


@router.get("/admin/rooms/list")
async def get_rooms_list(request: Request, role_of_current_user=Depends(get_role_of_current_user)):
    rooms = await RoomDAO.find_all()
    return templates.TemplateResponse(name="rooms-admin.html", context={"request": request, "rooms": rooms})


@router.get("/admin/hotels/add")
async def add_hotel(request: Request,  role_of_current_user=Depends(get_role_of_current_user)):
    return templates.TemplateResponse(name="add-hotel.html", context={"request": request})


@router.get("/admin/rooms/add")
async def add_room(request: Request, role_of_current_user=Depends(get_role_of_current_user)):
    return templates.TemplateResponse(name="add-room.html", context={"request": request, })


@router.get("/admin/hotels/add_images/{hotel_id}")
async def add_hotel(request: Request, hotel_id: int, role_of_current_user=Depends(get_role_of_current_user)):
    return templates.TemplateResponse(name="add-images-hotels.html", context={"request": request, "hotel_id": hotel_id})


@router.get("/admin/rooms/add_images/{room_id}")
async def add_room(request: Request, room_id: int, role_of_current_user=Depends(get_role_of_current_user)):
    return templates.TemplateResponse(name="add-images-rooms.html", context={"request": request, "room_id": room_id})
