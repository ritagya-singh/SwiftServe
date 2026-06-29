from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant


class RestaurantRepository:

    # -----------------------------
    # Create Restaurant
    # -----------------------------
    def create_restaurant(
        self,
        db: Session,
        restaurant: Restaurant
    ):
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        return restaurant

    # -----------------------------
    # Get Restaurant By ID
    # -----------------------------
    def get_restaurant_by_id(
        self,
        db: Session,
        restaurant_id: int
    ):
        return (
            db.query(Restaurant)
            .filter(Restaurant.id == restaurant_id)
            .first()
        )

    # -----------------------------
    # Get Restaurant By Email
    # -----------------------------
    def get_restaurant_by_email(
        self,
        db: Session,
        email: str
    ):
        return (
            db.query(Restaurant)
            .filter(Restaurant.email == email)
            .first()
        )

    # -----------------------------
    # Get All Restaurants
    # -----------------------------
    def get_all_restaurants(
        self,
        db: Session
    ):
        return (
            db.query(Restaurant)
            .order_by(Restaurant.id)
            .all()
        )

    # -----------------------------
    # Get Restaurants By Owner
    # -----------------------------
    def get_restaurants_by_owner(
        self,
        db: Session,
        owner_id: int
    ):
        return (
            db.query(Restaurant)
            .filter(Restaurant.owner_id == owner_id)
            .all()
        )

    # -----------------------------
    # Update Restaurant
    # -----------------------------
    def update_restaurant(
        self,
        db: Session,
        restaurant: Restaurant
    ):
        db.commit()
        db.refresh(restaurant)
        return restaurant

    # -----------------------------
    # Delete Restaurant
    # -----------------------------
    def delete_restaurant(
        self,
        db: Session,
        restaurant: Restaurant
    ):
        db.delete(restaurant)
        db.commit()