from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    # ===========================================
    # Create Category
    # ===========================================

    def create_category(
        self,
        db: Session,
        category: Category
    ):

        db.add(category)

        db.commit()

        db.refresh(category)

        return category

    # ===========================================
    # Get Category By ID
    # ===========================================

    def get_category_by_id(
        self,
        db: Session,
        category_id: int
    ):

        return (

            db.query(Category)

            .filter(Category.id == category_id)

            .first()

        )

    # ===========================================
    # Get Categories By Restaurant
    # ===========================================

    def get_categories_by_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):

        return (

            db.query(Category)

            .filter(
                Category.restaurant_id == restaurant_id
            )

            .order_by(Category.name)

            .all()

        )

    # ===========================================
    # Get Category By Name
    # ===========================================

    def get_category_by_name(
        self,
        db: Session,
        restaurant_id: int,
        name: str
    ):

        return (

            db.query(Category)

            .filter(

                Category.restaurant_id == restaurant_id,

                Category.name == name

            )

            .first()

        )

    # ===========================================
    # Update Category
    # ===========================================

    def update_category(
        self,
        db: Session,
        category: Category
    ):

        db.commit()

        db.refresh(category)

        return category

    # ===========================================
    # Delete Category
    # ===========================================

    def delete_category(
        self,
        db: Session,
        category: Category
    ):

        db.delete(category)

        db.commit()