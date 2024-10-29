from datetime import date, datetime
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.hotels.rooms.router import get_rooms
from app.hotels.router import get_hotel_by_id, get_hotels
from app.booking.router import get_bookings


router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def base(request: Request):
    return templates.TemplateResponse(name="base.html", context={"request": request})


@router.get("/main", response_class=HTMLResponse)
async def get_hotels_pages(request: Request):
    return templates.TemplateResponse(name="main.html", context={"request": request})


@router.get("/auth/register")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@router.get("/auth/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


# @router.get("/hotels")
# async def get_hotels_pages(request: Request, hotels=Depends(get_hotels)):
#     return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})


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
async def pay(request: Request, booking_id: str):
    return templates.TemplateResponse(name="pay.html", context={"request": request, "booking_id": booking_id})
