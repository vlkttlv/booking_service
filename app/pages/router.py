from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from app.booking.router import add_booking, get_bookings
# from app.hotels.rooms.router import get_rooms
# from app.hotels.router import get_hotel_by_id, get_hotels


router = APIRouter(
    prefix="/pages",
    tags=["Фронт"]
)

# templates = Jinja2Templates(directory="app/templates")


# @router.get("/hotels")
# async def get_hotels_pages(request: Request, hotels=Depends(get_hotels)):
#     return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})
