import stripe
from datetime import datetime
from pydantic import parse_obj_as
from fastapi import Depends, HTTPException, APIRouter

from app.booking.dao import BookingDAO
from app.booking.schemas import SBooking
from app.payments.dao import PaymentDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.config import settings
from app.tasks.tasks import send_pay_confirmation_email

router = APIRouter(
    prefix="/payments",
    tags=["Оплата"]
)

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/pay")
async def pay(token: str, booking_id: int, user: Users = Depends(get_current_user)):
    # Создаем платеж в Stripe
    try:
        booking = await BookingDAO.find_one_or_none(id=booking_id)
        charge = stripe.Charge.create(
            amount=booking.price,
            currency='rub',
            source=token,
            description='Бронирование отеля',
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Обновляем статус брони в БД
    await BookingDAO.update_table(booking_id=booking.id)

    # добавляем запись о платеже в БД
    await PaymentDAO.add(user_id=user.id, booking_id=booking.id,
                         amount=booking.price, date_to=datetime.now(), status="success")

    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_pay_confirmation_email.delay(
        booking=booking_dict, email_to=user.email)

    return {"message": "Оплата проведена успешно", "charge_id": charge.id}
