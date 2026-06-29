from datetime import datetime, timezone
import uuid

from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies import current_user
from app.models import order
from app.models import payment
from app.models.payment import (
    Payment,
    PaymentStatus,
    PaymentMethod
)

from app.models.order import Order

from app.models.user import User

from app.repositories.payment_repository import PaymentRepository

from app.repositories.order_repository import OrderRepository

class PaymentService:
    def __init__(self):

        self.payment_repository = PaymentRepository()

        self.order_repository = OrderRepository()
    def create_payment(
        self,
        db: Session,
        order_id: int,
        payment_method: PaymentMethod,
        current_user: User
    ):

        order = self.order_repository.get_by_id(
        db,
        order_id
    )

        if order is None:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

        if order.customer_id != current_user.id:

            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to pay for this order."
        )

        existing_payment = self.payment_repository.get_by_order(
        db,
        order_id
        )

        if existing_payment:

            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this order."
        )

        transaction_id = self._generate_transaction_id()
        payment = Payment(

        order_id=order.id,

        customer_id=current_user.id,

        amount=order.total_amount,

        payment_method=payment_method,

        payment_status=PaymentStatus.PENDING,

        transaction_id=transaction_id
    )

        return self.payment_repository.create(
        db,
        payment
    )

    def get_payment_by_id(
    self,
    db: Session,
    payment_id: int,
    current_user: User
    ):

        payment = self.payment_repository.get_by_id(
        db,
        payment_id
    )

        if payment is None:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

        order = payment.order

        if (
            payment.customer_id != current_user.id
            and
            order.restaurant.owner_id != current_user.id
        ):

            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this payment."
        )

        return payment
    def get_payment_by_order(
        self,
        db: Session,
        order_id: int,
        current_user: User
    ):

        order = self.order_repository.get_by_id(
        db,
        order_id
        )

        if order is None:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

        if (
            order.customer_id != current_user.id
            and
            order.restaurant.owner_id != current_user.id
        ):

            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this payment."
        )

        payment = self.payment_repository.get_by_order(
        db,
        order_id
        )

        if payment is None:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found for this order."
        )

        return payment
    def get_customer_payments(
    self,
    db: Session,
    current_user: User
    ):

        payments = self.payment_repository.get_customer_payments(
        db,
        current_user.id
        )

        return payments
    

    def update_payment_status(
    self,
    db: Session,
    payment_id: int,
    payment_status: PaymentStatus,
    current_user: User
    ):

        payment = self.payment_repository.get_by_id(
        db,
        payment_id
        )

        if payment is None:

            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

        order = payment.order

        if (
        payment.customer_id != current_user.id
        and
        order.restaurant.owner_id != current_user.id
        ):

            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this payment."
        )

        self._validate_payment_status_transition(
        payment.payment_status,
        payment_status
        )

        payment.payment_status = payment_status

        if payment_status == PaymentStatus.SUCCESS:

            payment.paid_at = datetime.now(timezone.utc)

        return self.payment_repository.update(
        db,
        payment
        )
    def _generate_transaction_id(self) -> str:

        return "TXN_" + uuid.uuid4().hex.upper()[:16]


    def _validate_payment_status_transition(
    self,
    current_status: PaymentStatus,
    new_status: PaymentStatus
    ):

        allowed_transitions = {

            PaymentStatus.PENDING: [
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED
        ],

            PaymentStatus.FAILED: [
            PaymentStatus.PENDING
        ],

            PaymentStatus.SUCCESS: [
            PaymentStatus.REFUNDED
        ],

        PaymentStatus.REFUNDED: []

    }

        if new_status not in allowed_transitions[current_status]:

            raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Invalid payment status transition."

        )


    def _verify_payment_access(
    self,
    payment: Payment,
    current_user: User
    ):

        if (

        payment.customer_id != current_user.id

        and

        payment.order.restaurant.owner_id != current_user.id

    ):

            raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="You are not allowed to access this payment."

        )