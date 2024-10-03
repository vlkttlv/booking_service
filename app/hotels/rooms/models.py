from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Rooms(Base):
    """Модель таблицы Комнаты"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    discription = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    sevices = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    # image_id = Column(Integer)

    hotel = relationship("Hotels", back_populates="room")
    booking = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Комната {self.name}"


class RoomsImages(Base):
    """Модель таблицы с изображенями для комнат"""
    __tablename__ = "rooms_images"

    id = Column(Integer, primary_key=True, nullable=False)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    image_id = Column(Integer, nullable=False)
