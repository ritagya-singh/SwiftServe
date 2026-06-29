from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.restaurant_schema import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
)
from app.services.restaurant_service import RestaurantService
from app.dependencies.current_user import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

service = RestaurantService()


# =====================================
# Create Restaurant
# =====================================

@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=201
)
def create_restaurant(

    request: RestaurantCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):
    return service.create_restaurant(
        db=db,
        current_user=current_user,
        request=request
    )


# =====================================
# Get All Restaurants
# =====================================

@router.get(
    "",
    response_model=List[RestaurantResponse]
)
def get_all_restaurants(
    db: Session = Depends(get_db)
):
    return service.get_all_restaurants(db)


# =====================================
# Get Restaurant By ID
# =====================================

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    return service.get_restaurant(
        db=db,
        restaurant_id=restaurant_id
    )


# =====================================
# Update Restaurant
# =====================================

@router.put(
    "/{restaurant_id}/owner/{owner_id}",
    response_model=RestaurantResponse
)
def update_restaurant(
    restaurant_id: int,
    request: RestaurantUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):
    return service.update_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
        request=request
    )


# =====================================
# Delete Restaurant
# =====================================

@router.delete(
    "/{restaurant_id}/owner/{owner_id}"
)
def delete_restaurant(
    restaurant_id: int,
    owner_id: int,
    db: Session = Depends(get_db)
):
    return service.delete_restaurant(
        db=db,
        restaurant_id=restaurant_id,
        owner_id=owner_id
    )