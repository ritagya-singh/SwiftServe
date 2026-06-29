from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant_schema import (
    RestaurantCreate,
    RestaurantUpdate,
)
from app.models.user import User


class RestaurantService:

    def __init__(self):
        self.repository = RestaurantRepository()

    # ====================================
    # Create Restaurant
    # ====================================

    def create_restaurant(
        self,
        db: Session,
        current_user: User,
        request: RestaurantCreate
    ):

        existing = self.repository.get_restaurant_by_email(
            db,
            request.email
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Restaurant email already exists."
            )

        restaurant = Restaurant(

            name=request.name,
            description=request.description,

            owner_id=current_user.id,

            phone=request.phone,
            email=request.email,

            address=request.address,
            city=request.city,
            state=request.state,
            pincode=request.pincode,

            opening_time=request.opening_time,
            closing_time=request.closing_time,

            is_open=True
        )

        return self.repository.create_restaurant(
            db,
            restaurant
        )

    # ====================================
    # Get Restaurant By ID
    # ====================================

    def get_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):

        restaurant = self.repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail="Restaurant not found."
            )

        return restaurant

    # ====================================
    # Get All Restaurants
    # ====================================

    def get_all_restaurants(
        self,
        db: Session
    ):

        return self.repository.get_all_restaurants(db)

    # ====================================
    # Update Restaurant
    # ====================================

    def update_restaurant(
        self,
        db: Session,
        restaurant_id: int,
        current_user,
        request: RestaurantUpdate
    ):

        restaurant = self.repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail="Restaurant not found."
            )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update this restaurant."
            )

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(
                restaurant,
                key,
                value
            )

        return self.repository.update_restaurant(
            db,
            restaurant
        )

    # ====================================
    # Delete Restaurant
    # ====================================

    def delete_restaurant(
        self,
        db: Session,
        restaurant_id: int,
        current_user
    ):

        restaurant = self.repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=404,
                detail="Restaurant not found."
            )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to delete this restaurant."
            )

        self.repository.delete_restaurant(
            db,
            restaurant
        )

        return {
            "message": "Restaurant deleted successfully."
        }