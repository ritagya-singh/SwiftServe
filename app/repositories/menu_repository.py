from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem


class MenuRepository:

    # ==========================================
    # Create Menu Item
    # ==========================================

    def create_menu_item(
        self,
        db: Session,
        menu_item: MenuItem
    ):
        db.add(menu_item)
        db.commit()
        db.refresh(menu_item)
        return menu_item

    # ==========================================
    # Get Menu Item By ID
    # ==========================================

    def get_menu_item_by_id(
        self,
        db: Session,
        menu_item_id: int
    ):
        return (
            db.query(MenuItem)
            .filter(MenuItem.id == menu_item_id)
            .first()
        )

    # ==========================================
    # Get Menu Item By Name
    # ==========================================

    def get_menu_item_by_name(
        self,
        db: Session,
        category_id: int,
        name: str
    ):
        return (
            db.query(MenuItem)
            .filter(
                MenuItem.category_id == category_id,
                MenuItem.name == name
            )
            .first()
        )

    # ==========================================
    # Get Menu Items By Restaurant
    # ==========================================

    def get_menu_items_by_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):
        return (
            db.query(MenuItem)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .all()
        )

    # ==========================================
    # Get Menu Items By Category
    # ==========================================

    def get_menu_items_by_category(
        self,
        db: Session,
        category_id: int
    ):
        return (
            db.query(MenuItem)
            .filter(MenuItem.category_id == category_id)
            .all()
        )

    # ==========================================
    # Update Menu Item
    # ==========================================

    def update_menu_item(
        self,
        db: Session,
        menu_item: MenuItem
    ):
        db.commit()
        db.refresh(menu_item)
        return menu_item

    # ==========================================
    # Delete Menu Item
    # ==========================================

    def delete_menu_item(
        self,
        db: Session,
        menu_item: MenuItem
    ):
        db.delete(menu_item)
        db.commit()