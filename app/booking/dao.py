#отдельный файл для работы с бд DAO

from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from app.dao.base import BaseDAO
from app.booking.models import Bookings
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker

class BookingDAO(BaseDAO):
    
    model = Bookings

    @classmethod
    async def find_all_with_images(cls, user_id: int):
        async with async_session_maker() as session:  
            '''
            SELECT *
            FROM  bookings  b left JOIN  rooms r ON b.room_id = r.id
            where b.user_id = 3; 
            -- 3 = user_id 
            '''       
            query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True) # isouter = left join
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()
        

    @classmethod
    async def add(cls, user_id:int, room_id: int,date_from: date,date_to: date):

    # -- сначала узнаем сколько свободных комнат осталось?
    # -- въезд 2024-06-25
    # -- выезд 2024-07-05
    # -- room 1

    # WITH booked_rooms AS (
    #     SELECT * FROM bookings
    #     WHERE room_id = 1 AND 
    #     (date_from >= '2024-06-25' AND date_from <= '2024-07-05') OR 
    #     (date_from <= '2024-06-25' AND date_to >= '2024-06-25' ) 
    # )

    # -- получаем все забронированные комнаты + их количесвто всего
    # -- select * from rooms
    # -- left join booked_rooms on rooms.id = booked_rooms.room_id
    # -- where rooms.id = 1

    # -- получаем количество совбодных комнат (всего кол-ва комнат - всего броней на комнату)
    # select rooms.quantity - COUNT(booked_rooms.room_id) from rooms
    # left join booked_rooms on rooms.id = booked_rooms.room_id
    # where rooms.id = 1
    # group by rooms.quantity
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id == room_id,
                    or_(
                        and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                        and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)
                    )
                )
            ).cte('booked_rooms')

            free_rooms = select(Rooms.quantity - func.count(booked_rooms.c.room_id)).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter = True).where(Rooms.id == room_id
                ).group_by(Rooms.quantity)

            result = await session.execute(free_rooms)
            free_rooms: int = result.scalar()
            if free_rooms > 0:

                get_price = select(Rooms.price).filter_by(id = room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()

                add_booking = insert(Bookings).values(
                    room_id = room_id,
                    user_id = user_id,
                    date_from = date_from,
                    date_to = date_to,
                    price = price
                ).returning(Bookings) # возвращает вставленную строку

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None



