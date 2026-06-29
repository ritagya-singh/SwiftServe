from sqlalchemy.orm import Session

from app.models.recipe_item import RecipeItem


class RecipeRepository:

    # =====================================================
    # Create Recipe Item
    # =====================================================

    def create_recipe_item(
        self,
        db: Session,
        recipe_item: RecipeItem
    ):

        db.add(recipe_item)

        db.commit()

        db.refresh(recipe_item)

        return recipe_item

    # =====================================================
    # Get Recipe Item By ID
    # =====================================================

    def get_recipe_item_by_id(
        self,
        db: Session,
        recipe_item_id: int
    ):

        return (

            db.query(RecipeItem)

            .filter(
                RecipeItem.id == recipe_item_id
            )

            .first()

        )

    # =====================================================
    # Get All Recipe Items Of Menu Item
    # =====================================================

    def get_recipe_items_by_menu_item(
        self,
        db: Session,
        menu_item_id: int
    ):

        return (

            db.query(RecipeItem)

            .filter(
                RecipeItem.menu_item_id == menu_item_id
            )

            .all()

        )

    # =====================================================
    # Get Recipe By Menu And Inventory Item
    # =====================================================

    def get_recipe_by_menu_and_inventory(
        self,
        db: Session,
        menu_item_id: int,
        inventory_item_id: int
    ):

        return (

            db.query(RecipeItem)

            .filter(

                RecipeItem.menu_item_id == menu_item_id,

                RecipeItem.inventory_item_id == inventory_item_id

            )

            .first()

        )

    # =====================================================
    # Update Recipe Item
    # =====================================================

    def update_recipe_item(
        self,
        db: Session,
        recipe_item: RecipeItem
    ):

        db.commit()

        db.refresh(recipe_item)

        return recipe_item

    # =====================================================
    # Delete Recipe Item
    # =====================================================

    def delete_recipe_item(
        self,
        db: Session,
        recipe_item: RecipeItem
    ):

        db.delete(recipe_item)

        db.commit()