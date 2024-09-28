from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin
from app.config import settings
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
# Добавить доп фильтрацию для поиска комнат
# добавить роль админа

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


@app.on_event("startup")
def startup():
    """
    не помню что делает
    """
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                              encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
