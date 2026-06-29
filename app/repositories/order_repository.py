from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:

    # =====================================================
    # Create Order
    # =====================================================

    def create_order(
        self,
        db: Session,
        order: Order
    ):

        db.add(order)

        db.flush()

        db.refresh(order)

        return order

    # =====================================================
    # Create Order Item
    # =====================================================

    def create_order_item(
        self,
        db: Session,
        order_item: OrderItem
    ):

        db.add(order_item)

        db.flush()

        db.refresh(order_item)

        return order_item

    # =====================================================
    # Get Order By ID
    # =====================================================

    def get_order_by_id(
        self,
        db: Session,
        order_id: int
    ):

        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    # =====================================================
    # Get Orders By Customer
    # =====================================================

    def get_orders_by_customer(
        self,
        db: Session,
        customer_id: int
    ):

        return (
            db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    # =====================================================
    # Get Orders By Restaurant
    # =====================================================

    def get_orders_by_restaurant(
        self,
        db: Session,
        restaurant_id: int
    ):

        return (
            db.query(Order)
            .filter(
                Order.restaurant_id == restaurant_id
            )
            .order_by(Order.created_at.desc())
            .all()
        )

    # =====================================================
    # Update Order
    # =====================================================

    def update_order(
        self,
        db: Session,
        order: Order
    ):

        db.flush()

        db.refresh(order)

        return order

    # =====================================================
    # Delete Order
    # =====================================================

    def delete_order(
        self,
        db: Session,
        order: Order
    ):

        db.delete(order)

        db.flush()