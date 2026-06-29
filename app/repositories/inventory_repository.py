from sqlalchemy.orm import Session

from app.models.inventory_item import InventoryItem


class InventoryRepository:

    # =====================================================
    # Create Inventory Item
    # =====================================================

    def create_inventory_item(
        self,
        db: Session,
        inventory_item: InventoryItem
    ):

        db.add(inventory_item)

        db.commit()

        db.refresh(inventory_item)

        return inventory_item

    # =====================================================
    # Get Inventory Item By ID
    # =====================================================

    def get_inventory_item_by_id(
        self,
        db: Session,
        inventory_item_id: int
    ):

        return (

            db.query(InventoryItem)

            .filter(
                InventoryItem.id == inventory_item_id
            )

            .first()

        )

    # =====================================================
    # Get Inventory Item By Ingredient Name
    # =====================================================

    def get_inventory_item_by_name(
        self,
        db: Session,
        restaurant_id: int,
        ingredient_name: str
    ):

        return (

            db.query(InventoryItem)

            .filter(

                InventoryItem.restaurant_id == restaurant_id,

                InventoryItem.ingredient_name == ingredient_name

            )

            .first()

        )

    # =====================================================
    # Get All Inventory Items Of Restaurant
    # =====================================================

    def get_inventory_items_by_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):

        return (

            db.query(InventoryItem)

            .filter(
                InventoryItem.restaurant_id == restaurant_id
            )

            .order_by(
                InventoryItem.ingredient_name
            )

            .all()

        )

    # =====================================================
    # Update Inventory Item
    # =====================================================

    def update_inventory_item(
        self,
        db: Session,
        inventory_item: InventoryItem
    ):

        db.commit()

        db.refresh(inventory_item)

        return inventory_item

    # =====================================================
    # Delete Inventory Item
    # =====================================================

    def delete_inventory_item(
        self,
        db: Session,
        inventory_item: InventoryItem
    ):

        db.delete(inventory_item)

        db.commit()