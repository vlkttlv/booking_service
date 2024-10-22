from datetime import date

from sqlalchemy import and_, func, or_, select

from backend.app.booking.models import Bookings
from backend.app.dao.base import BaseDAO
from backend.app.hotels.models import Hotels, HotelsImages
from backend.app.database import async_session_maker
from backend.app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):

    model = Hotels

    @classmethod
    async def find_all_by_location_and_date(cls, location: str, date_from: date, date_to: date, services: str,
                                            min_check: int = 0, max_check: int = 100000):
        """Получение всех отелей для указанной локации, дат и ценового диапазона."""
        booked_rooms = (
            select(Bookings.room_id, Bookings.price, func.count(
                Bookings.room_id).label("rooms_booked"))
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
            .group_by(Bookings.room_id, Bookings.price)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(Rooms.hotel_id, Rooms.price, func.sum(
                Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id, Rooms.price)
            .cte("booked_hotels")
        )
        # SELECT id, name, location, services, rooms_quantity, image_id, hotel_id, hotels.name, SUM(rooms_left) as room_left FROM hotels
        # LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        # WHERE rooms_left > 0 AND location LIKE '%Алтай%'
        # 	AND booked_hotels.price >= 0 AND booked_hotels.price <= 30000
        # 	AND 'Парковка' = ANY(services) AND array['Бассейн'] && CAST(services as text[])
        # GROUP BY id, hotel_id

        input_services = services.split(' ')
        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                func.sum(booked_hotels.c.rooms_left).label("rooms_left"),
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                    booked_hotels.c.price >= min_check,
                    booked_hotels.c.price <= max_check,
                    Hotels.services.contains(input_services)

                )
            )
            .group_by(Hotels.id, booked_hotels.c.hotel_id)
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()


class HotelImagesDAO(BaseDAO):

    model = HotelsImages
