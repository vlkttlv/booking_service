from sqladmin import ModelView

from backend.app.booking.models import Bookings
from backend.app.hotels.models import Hotels
from backend.app.hotels.rooms.models import Rooms
from backend.app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.role]+[Users.booking]
    column_details_exclude_list = [Users.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + \
        [Bookings.user, Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.room]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
