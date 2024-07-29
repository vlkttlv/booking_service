from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.admin.views import HotelsAdmin, RoomsAdmin, UsersAdmin, BookingsAdmin
from app.booking.router import router as router_bookings
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.hotels.rooms.router import router as router_rooms
from app.database import engine
from app.admin.auth import authentication_backend

app = FastAPI()



# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)




app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_rooms)

app.mount("/static", StaticFiles(directory="app/static"), "static")
# class SHotel(BaseModel):
#     address: str
#     name: str
#     stars: int

# class HotelsSearchArgs: # можно использовать этот класс в качестве схемы для гет запрсоов
#     def __init__(self,
#                 location: str,
#                 date_from: date,
#                 date_to: date,
#                 has_spa: Optional[bool] = None,
#                 stars: Optional[int] = Query(None, ge=1, le=5), 
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.has_spa = has_spa
#         self.stars = stars

# @app.get("/hotels", response_model=list[SHotel])
# def get_hotels(
#     search: HotelsSearchArgs = Depends()
# ):
#     hotels = [
#         {
#             "address": "ул. Вершинина, 2, Томск",
#             "name": "Roga_kopata",
#             "stars": 2,
#         }
#     ]
#     return hotels

# class SBooking(BaseModel): #схема
#     room_id: int
#     date_from: date
#     date_to: date

# @app.post("/boolings")
# def add_booking(booking: SBooking): # букинг имеет оформат схемы
#     pass



@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8",decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
