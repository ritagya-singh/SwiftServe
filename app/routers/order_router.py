from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user

from app.models.user import User

from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate
)

from app.services.order_service import OrderService

router = APIRouter(

    prefix="/orders",

    tags=["Orders"]

)

service = OrderService()


@router.post(
    "",
    response_model=OrderResponse
)
def place_order(

    request: OrderCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.place_order(

        db,

        current_user,

        request

    )





@router.get(
    "/me",
    response_model=list[OrderResponse]
)
def my_orders(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_customer_orders(

        db,

        current_user

    )


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[OrderResponse]
)
def restaurant_orders(

    restaurant_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_restaurant_orders(

        db,

        restaurant_id,

        current_user

    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(

    order_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.get_order_by_id(

        db,

        order_id,

        current_user

    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_status(

    order_id: int,

    request: OrderStatusUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return service.update_order_status(

        db,

        order_id,

        request.status,

        current_user

    )