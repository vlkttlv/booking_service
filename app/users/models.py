from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String, nullable=True, default='user')

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"
