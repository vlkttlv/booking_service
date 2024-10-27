from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.hotels.rooms.router import get_rooms
from app.hotels.router import get_hotels
from app.users.dependencies import get_current_user

# from app.booking.router import add_booking, get_bookings
# from app.hotels.rooms.router import get_rooms
# from app.hotels.router import get_hotel_by_id, get_hotels


router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_hotels_pages(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(name="base.html", context={"request": request, "curent_user": current_user})


@router.get("/main")
async def get_hotels_pages(request: Request):
    return templates.TemplateResponse(name="main.html", context={"request": request})


@router.get("/hotels")
async def get_hotels_pages(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})


@router.get("/rooms")
async def get_rooms_pages(request: Request, rooms=Depends(get_rooms), hotel=Depends(get_hotels)):
    return templates.TemplateResponse(name="rooms.html", context={"request": request, "rooms": rooms, "hotel": hotel})


@router.get("/auth/register")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", context={"request": request})


@router.get("/auth/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("")
async def base(request: Request):
    return templates.TemplateResponse(name="base.html", context={"request": request})
