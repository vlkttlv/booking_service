from typing import Annotated
import stripe
from datetime import datetime
from pydantic import parse_obj_as
from fastapi import Depends, HTTPException, APIRouter, Header

from app.booking.dao import BookingDAO
from app.booking.schemas import SBooking
from app.exceptions import BookingAlreadyPaid
from app.payments.dao import PaymentDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.config import settings
from app.tasks.tasks import send_pay_confirmation_email
from app.logger import logger
router = APIRouter(
    prefix="/payments",
    tags=["Оплата"]
)

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/pay")
async def pay(booking_id: int, stripe_token: Annotated[str | None, Header()] = None, user: Users = Depends(get_current_user)):
    # Создаем платеж в Stripe
    try:
        booking = await BookingDAO.find_one_or_none(id=booking_id)

        if booking.payment_status == "not paid":
            if stripe_token == None:       # если запрос отправится с api, то в заголовке ничего не будет,
                stripe_token = 'tok_visa'  # поэтому присваиваем токену тестовое значение
            charge = stripe.Charge.create(
                amount=booking.total_cost,
                currency='rub',
                source=stripe_token,
                description='Бронирование отеля',
            )
        else:
            raise BookingAlreadyPaid

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Обновляем статус брони в БД
    await BookingDAO.update_table(booking_id=booking.id)

    # добавляем запись о платеже в БД
    await PaymentDAO.add(user_id=user.id, booking_id=booking.id,
                         amount=booking.total_cost, date_to=datetime.now(), status="success")

    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_pay_confirmation_email.delay(
        booking=booking_dict, email_to=user.email)
    logger.info(f"Бронь #{booking.id} была успешно оплачена")
    return {"message": "Оплата проведена успешно", "charge_id": charge.id}
