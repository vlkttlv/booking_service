import json
import os
import stripe
from fastapi import Depends, responses, Request, HTTPException, APIRouter

from backend.app.users.dependencies import get_current_user
from backend.app.users.models import Users
from config import settings

router = APIRouter(
    prefix="/payments",
    tags=["Оплата"]
)

# Replace with your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/process-payment/")
async def process_payment(amount: int, token: str, user: Users = Depends(get_current_user)):
    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency='rub',
            # Stripe token obtained from the client-side (e.g., Stripe.js)
            source=token,
            description="Payment for FastAPI Store",  # Add a description for the payment
            receipt_email=user.email,
        )

        # You can handle the charge object as per your requirements
        # For example, log the payment or perform other actions

        # Return a success response
        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        # Handle specific Stripe errors
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        # Handle generic Stripe errors
        return {"status": "error", "message": "Something went wrong. Please try again later."}
