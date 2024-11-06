import time
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI, version

from redis import asyncio as aioredis
from sqladmin import Admin
from app.config import settings
from app.admin.views import HotelsAdmin, PaymentsAdmin, RoomsAdmin, UsersAdmin, BookingsAdmin
from app.booking.router import router as router_bookings
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.hotels.rooms.router import router as router_rooms
from app.payments.router import router as router_payment
from app.database import engine
from app.admin.auth import authentication_backend
from app.logger import logger
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()

# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_payment)
app.include_router(router_pages)
app.include_router(router_images)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                              encoding="utf8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await (call_next(request))
    process_time = time.time() - start_time
    # response.headers['X-Process-Time'] = str(process_time) # это можно добавить в лог
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)})
    return response

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       )

# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(PaymentsAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")
