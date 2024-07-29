from datetime import date
from sqlalchemy import and_, func, or_, select

from app.booking.models import Bookings
from app.database import async_session_maker
from app.dao.base import BaseDAO


from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )
            get_rooms = (select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
                (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(
                Rooms.hotel_id == hotel_id
            )
        )

            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
