# from datetime import date, datetime, timedelta
# from fastapi import APIRouter, Depends, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# from app.hotels.rooms.router import get_rooms
# from app.hotels.router import get_hotels

# # from app.booking.router import add_booking, get_bookings
# # from app.hotels.rooms.router import get_rooms
# # from app.hotels.router import get_hotel_by_id, get_hotels


# router = APIRouter(
#     prefix="/pages",
#     tags=["Фронт"]
# )

# templates = Jinja2Templates(directory="app/templates")


# @router.get("/hotels")
# async def get_hotels_pages(request: Request, hotels=Depends(get_hotels)):
#     return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})


# @router.get("/rooms")
# async def get_rooms_pages(request: Request, rooms=Depends(get_rooms), hotel=Depends(get_hotels)):
#     return templates.TemplateResponse(name="rooms.html", context={"request": request, "rooms": rooms, "hotel": hotel})


# @router.get("/auth/register")
# async def register(request: Request):
#     return templates.TemplateResponse(name="register.html", context={"request": request})


# @router.get("/auth/login")
# async def login(request: Request):
#     return templates.TemplateResponse(name="login.html", context={"request": request})


# @router.get("")
# async def base(request: Request):
#     return templates.TemplateResponse(name="base.html", context={"request": request})


from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.app.booking.router import add_booking, get_bookings
from backend.app.hotels.rooms.router import get_rooms
from backend.app.hotels.router import get_hotel_by_id, get_hotels


def get_month_days(date: datetime = datetime.today()):
    counter = datetime(date.year, date.month,
                       datetime.today().day, tzinfo=date.tzinfo)
    date_list = []
    for _ in range(365*2):
        date_list.append(
            {"date": counter.date(), "date_formatted": counter.strftime("%Y-%m-%d")}
        )
        counter += timedelta(days=1)
    return date_list


def format_number_thousand_separator(
    number: int,
    separator: str = " ",
):
    return f"{number:,}".replace(",", separator)


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(
    request: Request,
    location: str,
    date_to: date,
    date_from: date,
    hotels=Depends(get_hotels),
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    # Автоматически ставим дату заезда позже текущей даты
    date_from = max(datetime.today().date(), date_from)
    # Автоматически ставим дату выезда не позже, чем через 180 дней
    date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)
    return templates.TemplateResponse(
        "hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_to": date_to.strftime("%Y-%m-%d"),
            "date_from": date_from.strftime("%Y-%m-%d"),
            "dates": dates,
        },
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
    request: Request,
    date_from: date,
    date_to: date,
    rooms=Depends(get_rooms),
    hotel=Depends(get_hotel_by_id),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
        },
    )


@router.post("/successful_booking", response_class=HTMLResponse)
async def get_successful_booking_page(
    request: Request,
    _=Depends(add_booking),
):
    return templates.TemplateResponse(
        "booking_successful.html", {"request": request}
    )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
    request: Request,
    bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
