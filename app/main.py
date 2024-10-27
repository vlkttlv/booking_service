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
from app.logger import logger
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()

origins = ["http://localhost:5173"]

# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=["*"]
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/")
def options():
    return {"allowed_origin": "http://localhost:5173"}


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_rooms)

# @app.on_event("startup")
# async def startup():
#     """
#     не помню что делает
#     """
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
#                               encoding="utf8", decode_response=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")

# ...


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await (call_next(request))
#     process_time = time.time() - start_time
#     # response.headers['X-Process-Time'] = str(process_time) # это можно добавить в лог
#     logger.info("Request execution time", extra={
#         "process_time": round(process_time, 4)})
#     return response

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       #    description="Greet users with a nice message"
                       )

# Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)
app.mount("/static", StaticFiles(directory="app/static"), "static")
