from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user

from app.models.user import User

from app.schemas.payment_schema import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate
)

from app.services.payment_service import PaymentService

router = APIRouter(

    prefix="/payments",

    tags=["Payments"]

)

service = PaymentService()


@router.post(
    "/order/{order_id}",
    response_model=PaymentResponse
)
def create_payment(

    order_id: int,

    request: PaymentCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.create_payment(

        db,

        order_id,

        request.payment_method,

        current_user

    )


@router.get(
    "/me",
    response_model=list[PaymentResponse]
)
def my_payments(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_customer_payments(

        db,

        current_user

    )


@router.get(
    "/order/{order_id}",
    response_model=PaymentResponse
)
def get_payment_by_order(

    order_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_payment_by_order(

        db,

        order_id,

        current_user

    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(

    payment_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_payment_by_id(

        db,

        payment_id,

        current_user

    )


@router.patch(
    "/{payment_id}/status",
    response_model=PaymentResponse
)
def update_payment_status(

    payment_id: int,

    request: PaymentStatusUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.update_payment_status(

        db,

        payment_id,

        request.payment_status,

        current_user

    )