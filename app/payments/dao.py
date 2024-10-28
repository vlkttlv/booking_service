from app.dao.base import BaseDAO
from app.payments.models import Payments


class PaymentDAO(BaseDAO):

    model = Payments
