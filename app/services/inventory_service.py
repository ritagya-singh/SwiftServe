from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.inventory_item import InventoryItem
from app.models.user import User

from app.repositories.inventory_repository import InventoryRepository
from app.repositories.restaurant_repository import RestaurantRepository

from app.schemas.inventory_schema import (
    InventoryItemCreate,
    InventoryItemUpdate
)


class InventoryService:

    def __init__(self):

        self.inventory_repository = InventoryRepository()

        self.restaurant_repository = RestaurantRepository()

    # =====================================================
    # Create Inventory Item
    # =====================================================

    def create_inventory_item(
        self,
        db: Session,
        restaurant_id: int,
        current_user: User,
        request: InventoryItemCreate
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
                detail="You are not allowed to manage this inventory."
            )

        # ---------------------------------------------
        # Step 3 : Check Duplicate Ingredient
        # ---------------------------------------------

        existing_item = (
            self.inventory_repository.get_inventory_item_by_name(
                db,
                restaurant_id,
                request.ingredient_name
            )
        )

        if existing_item:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient already exists."
            )

        # ---------------------------------------------
        # Step 4 : Create Inventory Object
        # ---------------------------------------------

        inventory_item = InventoryItem(

            restaurant_id=restaurant.id,

            ingredient_name=request.ingredient_name,

            unit=request.unit,

            quantity=request.quantity,

            minimum_quantity=request.minimum_quantity,

            is_active=request.is_active
        )

        # ---------------------------------------------
        # Step 5 : Save To Database
        # ---------------------------------------------

        return self.inventory_repository.create_inventory_item(
            db,
            inventory_item
        )
        # =====================================================
    # Get Inventory Item By ID
    # =====================================================

    def get_inventory_item(
        self,
        db: Session,
        inventory_item_id: int
    ):

        inventory_item = (
            self.inventory_repository.get_inventory_item_by_id(
                db,
                inventory_item_id
            )
        )

        if inventory_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )

        return inventory_item
        # =====================================================
    # Get All Inventory Items Of Restaurant
    # =====================================================

    def get_inventory_items_by_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        return (
            self.inventory_repository.get_inventory_items_by_restaurant(
                db,
                restaurant_id
            )
        )
        # =====================================================
    # Update Inventory Item
    # =====================================================

    def update_inventory_item(
        self,
        db: Session,
        inventory_item_id: int,
        current_user: User,
        request: InventoryItemUpdate
    ):

        # ---------------------------------------------
        # Step 1 : Check Inventory Item Exists
        # ---------------------------------------------

        inventory_item = (
            self.inventory_repository.get_inventory_item_by_id(
                db,
                inventory_item_id
            )
        )

        if inventory_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )

        # ---------------------------------------------
        # Step 2 : Get Restaurant
        # ---------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                inventory_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # ---------------------------------------------
        # Step 3 : Verify Restaurant Owner
        # ---------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this inventory."
            )

        # ---------------------------------------------
        # Step 4 : Duplicate Ingredient Check
        # ---------------------------------------------

        if request.ingredient_name is not None:

            existing_item = (
                self.inventory_repository.get_inventory_item_by_name(
                    db,
                    restaurant.id,
                    request.ingredient_name
                )
            )

            if (
                existing_item
                and existing_item.id != inventory_item.id
            ):

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ingredient already exists."
                )

        # ---------------------------------------------
        # Step 5 : Update Only Provided Fields
        # ---------------------------------------------

        update_data = request.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(
                inventory_item,
                key,
                value
            )

        # ---------------------------------------------
        # Step 6 : Save Changes
        # ---------------------------------------------

        return self.inventory_repository.update_inventory_item(
            db,
            inventory_item
        )
        # =====================================================
    # Delete Inventory Item
    # =====================================================

    def delete_inventory_item(
        self,
        db: Session,
        inventory_item_id: int,
        current_user: User
    ):

        # ---------------------------------------------
        # Step 1 : Check Inventory Item Exists
        # ---------------------------------------------

        inventory_item = (
            self.inventory_repository.get_inventory_item_by_id(
                db,
                inventory_item_id
            )
        )

        if inventory_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )

        # ---------------------------------------------
        # Step 2 : Get Restaurant
        # ---------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                inventory_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # ---------------------------------------------
        # Step 3 : Verify Restaurant Owner
        # ---------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this inventory item."
            )

        # ---------------------------------------------
        # Step 4 : Delete Inventory Item
        # ---------------------------------------------

        self.inventory_repository.delete_inventory_item(
            db,
            inventory_item
        )

        # ---------------------------------------------
        # Step 5 : Return Success Message
        # ---------------------------------------------

        return {
            "message": "Inventory item deleted successfully."
        }
    