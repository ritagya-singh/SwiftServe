from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.models.user import User

from app.repositories.menu_repository import MenuRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.category_repository import CategoryRepository

from app.schemas.menu_schema import (
    MenuItemCreate,
    MenuItemUpdate
)


class MenuService:

    def __init__(self):

        self.menu_repository = MenuRepository()

        self.restaurant_repository = RestaurantRepository()

        self.category_repository = CategoryRepository()

    # =====================================================
    # Create Menu Item
    # =====================================================

    def create_menu_item(
        self,
        db: Session,
        restaurant_id: int,
        current_user: User,
        request: MenuItemCreate
    ):

        # ---------------------------------------------
        # Step 1 : Check Restaurant Exists
        # ---------------------------------------------

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            restaurant_id
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # ---------------------------------------------
        # Step 2 : Verify Restaurant Owner
        # ---------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to add menu items."
            )

        # ---------------------------------------------
        # Step 3 : Check Category Exists
        # ---------------------------------------------

        category = self.category_repository.get_category_by_id(
            db,
            request.category_id
        )

        if category is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

        # ---------------------------------------------
        # Step 4 : Verify Category Belongs To Restaurant
        # ---------------------------------------------

        if category.restaurant_id != restaurant.id:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not belong to this restaurant."
            )

        # ---------------------------------------------
        # Step 5 : Prevent Duplicate Menu Item
        # ---------------------------------------------

        existing_menu_item = (
            self.menu_repository.get_menu_item_by_name(
                db,
                request.category_id,
                request.name
            )
        )

        if existing_menu_item:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu item already exists in this category."
            )

        # ---------------------------------------------
        # Step 6 : Create Menu Item Object
        # ---------------------------------------------

        menu_item = MenuItem(

            restaurant_id=restaurant.id,

            category_id=request.category_id,

            name=request.name,

            description=request.description,

            price=request.price,

            preparation_time=request.preparation_time,

            image_url=request.image_url,

            is_available=request.is_available
        )

        # ---------------------------------------------
        # Step 7 : Save Into Database
        # ---------------------------------------------

        return self.menu_repository.create_menu_item(
            db,
            menu_item
        )
    
        # =====================================================
    # Get Menu Item By ID
    # =====================================================

    def get_menu_item(
        self,
        db: Session,
        menu_item_id: int
    ):

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        return menu_item
    
        # =====================================================
    # Get All Menu Items Of Restaurant
    # =====================================================

    def get_menu_items_by_restaurant(
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

        return self.menu_repository.get_menu_items_by_restaurant(
            db,
            restaurant_id
        )
        # =====================================================
    # Get Menu Items By Category
    # =====================================================

    def get_menu_items_by_category(
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

        return self.menu_repository.get_menu_items_by_category(
            db,
            category_id
        )
        # =====================================================
    # Update Menu Item
    # =====================================================

    def update_menu_item(
        self,
        db: Session,
        menu_item_id: int,
        current_user: User,
        request: MenuItemUpdate
    ):

        # ---------------------------------------------
        # Step 1 : Check Menu Item Exists
        # ---------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # ---------------------------------------------
        # Step 2 : Get Restaurant
        # ---------------------------------------------

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            menu_item.restaurant_id
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # ---------------------------------------------
        # Step 3 : Verify Owner
        # ---------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this menu item."
            )

        # ---------------------------------------------
        # Step 4 : Check New Category (If Provided)
        # ---------------------------------------------

        if request.category_id is not None:

            category = self.category_repository.get_category_by_id(
                db,
                request.category_id
            )

            if category is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found."
                )

            if category.restaurant_id != restaurant.id:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category does not belong to this restaurant."
                )

        else:

            category = self.category_repository.get_category_by_id(
                db,
                menu_item.category_id
            )

        # ---------------------------------------------
        # Step 5 : Duplicate Name Check
        # ---------------------------------------------

        if request.name is not None:

            existing_item = self.menu_repository.get_menu_item_by_name(
                db,
                category.id,
                request.name
            )

            if (
                existing_item
                and existing_item.id != menu_item.id
            ):

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item already exists in this category."
                )

        # ---------------------------------------------
        # Step 6 : Update Fields
        # ---------------------------------------------

        update_data = request.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(
                menu_item,
                key,
                value
            )

        # ---------------------------------------------
        # Step 7 : Save Changes
        # ---------------------------------------------

        return self.menu_repository.update_menu_item(
            db,
            menu_item
        )
        # =====================================================
    # Delete Menu Item
    # =====================================================

    def delete_menu_item(
        self,
        db: Session,
        menu_item_id: int,
        current_user: User
    ):

        # ---------------------------------------------
        # Step 1 : Check Menu Item Exists
        # ---------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # ---------------------------------------------
        # Step 2 : Get Restaurant
        # ---------------------------------------------

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            menu_item.restaurant_id
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # ---------------------------------------------
        # Step 3 : Verify Owner
        # ---------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this menu item."
            )

        # ---------------------------------------------
        # Step 4 : Delete Menu Item
        # ---------------------------------------------

        self.menu_repository.delete_menu_item(
            db,
            menu_item
        )

        # ---------------------------------------------
        # Step 5 : Return Success Response
        # ---------------------------------------------

        return {
            "message": "Menu item deleted successfully."
        }