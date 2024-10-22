from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Hotels(Base):
    """Модель отеля"""
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(ARRAY(String))
    rooms_quantity = Column(Integer, nullable=False)
    # image_id = Column(Integer)

    room = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"Отель {self.name} {self.location}"


class HotelsImages(Base):
    """Модель таблицы с изображениями для отелей"""
    __tablename__ = "hotels_images"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    image_id = Column(Integer)
