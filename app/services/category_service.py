from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User

from app.repositories.category_repository import CategoryRepository
from app.repositories.restaurant_repository import RestaurantRepository

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate
)


class CategoryService:

    def __init__(self):

        self.category_repository = CategoryRepository()

        self.restaurant_repository = RestaurantRepository()

    # =====================================================
    # Create Category
    # =====================================================

    def create_category(
        self,
        db: Session,
        restaurant_id: int,
        current_user: User,
        request: CategoryCreate
    ):

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to create categories for this restaurant."
            )

        existing_category = self.category_repository.get_category_by_name(
            db,
            restaurant_id,
            request.name
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists."
            )

        category = Category(
            restaurant_id=restaurant.id,
            name=request.name,
            description=request.description
        )

        return self.category_repository.create_category(
            db,
            category
        )

    # =====================================================
    # Get All Categories Of Restaurant
    # =====================================================

    def get_categories(
        self,
        db: Session,
        restaurant_id: int
    ):

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        return self.category_repository.get_categories_by_restaurant(
            db,
            restaurant_id
        )

    # =====================================================
    # Get Category By ID
    # =====================================================

    def get_category(
        self,
        db: Session,
        category_id: int
    ):

        category = self.category_repository.get_category_by_id(
            db,
            category_id
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        return category

    # =====================================================
    # Update Category
    # =====================================================

    def update_category(
        self,
        db: Session,
        category_id: int,
        current_user: User,
        request: CategoryUpdate
    ):

        category = self.category_repository.get_category_by_id(
            db,
            category_id
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            category.restaurant_id
        )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this category."
            )

        if (
            request.name is not None
            and request.name != category.name
        ):

            existing_category = self.category_repository.get_category_by_name(
                db,
                restaurant.id,
                request.name
            )

            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category already exists."
                )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                category,
                key,
                value
            )

        return self.category_repository.update_category(
            db,
            category
        )

    # =====================================================
    # Delete Category
    # =====================================================

    def delete_category(
        self,
        db: Session,
        category_id: int,
        current_user: User
    ):

        category = self.category_repository.get_category_by_id(
            db,
            category_id
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            category.restaurant_id
        )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this category."
            )

        self.category_repository.delete_category(
            db,
            category
        )

        return {
            "message": "Category deleted successfully."
        }