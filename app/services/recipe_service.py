from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.recipe_item import RecipeItem
from app.models.user import User

from app.repositories.recipe_repository import RecipeRepository
from app.repositories.menu_repository import MenuRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.restaurant_repository import RestaurantRepository

from app.schemas.recipe_schema import (
    RecipeItemCreate,
    RecipeItemUpdate
)
class RecipeService:

    def __init__(self):

        self.recipe_repository = RecipeRepository()

        self.menu_repository = MenuRepository()

        self.inventory_repository = InventoryRepository()

        self.restaurant_repository = RestaurantRepository()

        # =====================================================
    # Create Recipe Item
    # =====================================================

    def create_recipe_item(
        self,
        db: Session,
        menu_item_id: int,
        current_user: User,
        request: RecipeItemCreate
    ):

        # -------------------------------------------------
        # Step 1 : Check Menu Item Exists
        # -------------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # -------------------------------------------------
        # Step 2 : Check Inventory Item Exists
        # -------------------------------------------------

        inventory_item = (
            self.inventory_repository.get_inventory_item_by_id(
                db,
                request.inventory_item_id
            )
        )

        if inventory_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )

        # -------------------------------------------------
        # Step 3 : Both Must Belong To Same Restaurant
        # -------------------------------------------------

        if menu_item.restaurant_id != inventory_item.restaurant_id:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu item and inventory item belong to different restaurants."
            )

        # -------------------------------------------------
        # Step 4 : Verify Restaurant Owner
        # -------------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                menu_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify this recipe."
            )

        # -------------------------------------------------
        # Step 5 : Prevent Duplicate Ingredient
        # -------------------------------------------------

        existing_recipe = (
            self.recipe_repository.get_recipe_by_menu_and_inventory(
                db,
                menu_item.id,
                request.inventory_item_id
            )
        )

        if existing_recipe:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient already added to this recipe."
            )

        # -------------------------------------------------
        # Step 6 : Create Recipe Object
        # -------------------------------------------------

        recipe_item = RecipeItem(

            menu_item_id=menu_item.id,

            inventory_item_id=request.inventory_item_id,

            quantity_required=request.quantity_required
        )

        # -------------------------------------------------
        # Step 7 : Save
        # -------------------------------------------------

        return self.recipe_repository.create_recipe_item(
            db,
            recipe_item
        )
        # =====================================================
    # Create Recipe Item
    # =====================================================

    def create_recipe_item(
        self,
        db: Session,
        menu_item_id: int,
        current_user: User,
        request: RecipeItemCreate
    ):

        # -------------------------------------------------
        # Step 1 : Check Menu Item Exists
        # -------------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # -------------------------------------------------
        # Step 2 : Check Inventory Item Exists
        # -------------------------------------------------

        inventory_item = (
            self.inventory_repository.get_inventory_item_by_id(
                db,
                request.inventory_item_id
            )
        )

        if inventory_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found."
            )

        # -------------------------------------------------
        # Step 3 : Both Must Belong To Same Restaurant
        # -------------------------------------------------

        if menu_item.restaurant_id != inventory_item.restaurant_id:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Menu item and inventory item belong to different restaurants."
            )

        # -------------------------------------------------
        # Step 4 : Verify Restaurant Owner
        # -------------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                menu_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify this recipe."
            )

        # -------------------------------------------------
        # Step 5 : Prevent Duplicate Ingredient
        # -------------------------------------------------

        existing_recipe = (
            self.recipe_repository.get_recipe_by_menu_and_inventory(
                db,
                menu_item.id,
                request.inventory_item_id
            )
        )

        if existing_recipe:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient already added to this recipe."
            )

        # -------------------------------------------------
        # Step 6 : Create Recipe Object
        # -------------------------------------------------

        recipe_item = RecipeItem(

            menu_item_id=menu_item.id,

            inventory_item_id=request.inventory_item_id,

            quantity_required=request.quantity_required
        )

        # -------------------------------------------------
        # Step 7 : Save
        # -------------------------------------------------

        return self.recipe_repository.create_recipe_item(
            db,
            recipe_item
        )
        # =====================================================
    # Get All Recipe Items Of Menu Item
    # =====================================================

    def get_recipe_items_by_menu_item(
        self,
        db: Session,
        menu_item_id: int
    ):

        menu_item = (
            self.menu_repository.get_menu_item_by_id(
                db,
                menu_item_id
            )
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        return (
            self.recipe_repository.get_recipe_items_by_menu_item(
                db,
                menu_item_id
            )
        )
        # =====================================================
    # Update Recipe Item
    # =====================================================

    def update_recipe_item(
        self,
        db: Session,
        recipe_item_id: int,
        current_user: User,
        request: RecipeItemUpdate
    ):

        # -------------------------------------------------
        # Step 1 : Check Recipe Item Exists
        # -------------------------------------------------

        recipe_item = (
            self.recipe_repository.get_recipe_item_by_id(
                db,
                recipe_item_id
            )
        )

        if recipe_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe item not found."
            )

        # -------------------------------------------------
        # Step 2 : Get Menu Item
        # -------------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            recipe_item.menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # -------------------------------------------------
        # Step 3 : Get Restaurant
        # -------------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                menu_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # -------------------------------------------------
        # Step 4 : Verify Restaurant Owner
        # -------------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this recipe."
            )

        # -------------------------------------------------
        # Step 5 : Validate New Inventory Item
        # -------------------------------------------------

        if request.inventory_item_id is not None:

            inventory_item = (
                self.inventory_repository.get_inventory_item_by_id(
                    db,
                    request.inventory_item_id
                )
            )

            if inventory_item is None:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Inventory item not found."
                )

            if inventory_item.restaurant_id != menu_item.restaurant_id:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Inventory item belongs to another restaurant."
                )

            existing_recipe = (
                self.recipe_repository.get_recipe_by_menu_and_inventory(
                    db,
                    menu_item.id,
                    request.inventory_item_id
                )
            )

            if (
                existing_recipe
                and existing_recipe.id != recipe_item.id
            ):

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ingredient already exists in this recipe."
                )

        # -------------------------------------------------
        # Step 6 : Partial Update
        # -------------------------------------------------

        update_data = request.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(
                recipe_item,
                key,
                value
            )

        # -------------------------------------------------
        # Step 7 : Save Changes
        # -------------------------------------------------

        return self.recipe_repository.update_recipe_item(
            db,
            recipe_item
        )
        # =====================================================
    # Delete Recipe Item
    # =====================================================

    def delete_recipe_item(
        self,
        db: Session,
        recipe_item_id: int,
        current_user: User
    ):

        # -------------------------------------------------
        # Step 1 : Check Recipe Item Exists
        # -------------------------------------------------

        recipe_item = (
            self.recipe_repository.get_recipe_item_by_id(
                db,
                recipe_item_id
            )
        )

        if recipe_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe item not found."
            )

        # -------------------------------------------------
        # Step 2 : Get Menu Item
        # -------------------------------------------------

        menu_item = self.menu_repository.get_menu_item_by_id(
            db,
            recipe_item.menu_item_id
        )

        if menu_item is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found."
            )

        # -------------------------------------------------
        # Step 3 : Get Restaurant
        # -------------------------------------------------

        restaurant = (
            self.restaurant_repository.get_restaurant_by_id(
                db,
                menu_item.restaurant_id
            )
        )

        if restaurant is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        # -------------------------------------------------
        # Step 4 : Verify Restaurant Owner
        # -------------------------------------------------

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this recipe."
            )

        # -------------------------------------------------
        # Step 5 : Delete Recipe Item
        # -------------------------------------------------

        self.recipe_repository.delete_recipe_item(
            db,
            recipe_item
        )

        # -------------------------------------------------
        # Step 6 : Return Success
        # -------------------------------------------------

        return {
            "message": "Recipe item deleted successfully."
        }