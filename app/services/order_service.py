from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.dependencies import current_user
from app.models import restaurant
from app.models import order
from app.models import order
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User

from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_repository import MenuRepository
from app.repositories.recipe_repository import RecipeRepository
from app.repositories.inventory_repository import InventoryRepository

from app.schemas.order_schema import OrderCreate

class OrderService:

    def __init__(self):

        self.order_repository = OrderRepository()

        self.restaurant_repository = RestaurantRepository()

        self.menu_repository = MenuRepository()

        self.recipe_repository = RecipeRepository()

        self.inventory_repository = InventoryRepository()

        # =====================================================
    # Place Order
    # =====================================================

    def place_order(
        self,
        db: Session,
        current_user: User,
        request: OrderCreate
    ):
        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            request.restaurant_id
        )

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found."
            )

        if len(request.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item."
            )

        total_amount = 0
        validated_items = []

        for item in request.items:
            menu_item = self.menu_repository.get_menu_item_by_id(
                db,
                item.menu_item_id
            )

            if menu_item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu item {item.menu_item_id} not found."
                )

            if menu_item.restaurant_id != request.restaurant_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item belongs to another restaurant."
                )

            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{menu_item.name} is unavailable."
                )

            item_total = menu_item.price * item.quantity
            total_amount += item_total
            validated_items.append({
                "menu_item": menu_item,
                "quantity": item.quantity,
                "unit_price": menu_item.price,
                "total_price": item_total
            })

        for item in validated_items:
            menu_item = item["menu_item"]
            quantity = item["quantity"]

            recipe_items = self.recipe_repository.get_recipe_items_by_menu_item(
                db,
                menu_item.id
            )

            if len(recipe_items) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{menu_item.name} has no recipe configured."
                )

            for recipe in recipe_items:
                inventory_item = self.inventory_repository.get_inventory_item_by_id(
                    db,
                    recipe.inventory_item_id
                )

                if inventory_item is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Inventory item not found."
                    )

                required_quantity = recipe.quantity_required * quantity
                if inventory_item.quantity < required_quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Not enough {inventory_item.name}. "
                            f"Required: {required_quantity}, "
                            f"Available: {inventory_item.quantity}"
                        )
                    )

        try:
            order = Order(
                restaurant_id=request.restaurant_id,
                customer_id=current_user.id,
                total_amount=total_amount,
                status="PLACED"
            )

            self.order_repository.create_order(
                db,
                order
            )

            for item in validated_items:
                menu_item = item["menu_item"]
                quantity = item["quantity"]
                unit_price = item["unit_price"]
                total_price = item["total_price"]

                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )

                self.order_repository.create_order_item(
                    db,
                    order_item
                )

                recipe_items = self.recipe_repository.get_recipe_items_by_menu_item(
                    db,
                    menu_item.id
                )
                for recipe in recipe_items:
                    inventory_item = self.inventory_repository.get_inventory_item_by_id(
                        db,
                        recipe.inventory_item_id
                    )

                    inventory_item.quantity -= recipe.quantity_required * quantity
                    self.inventory_repository.update_inventory_item(
                        db,
                        inventory_item
                    )

            db.flush()
            db.refresh(order)

            return order
        except Exception:
            db.rollback()
            raise
        # =====================================================
    # Get Order By ID
    # =====================================================

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
        current_user: User
    ):

        order = self.order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )

        # Customer can view their own order
        if order.customer_id == current_user.id:
            return order

        # Restaurant owner can view restaurant orders
        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            order.restaurant_id
        )

        if restaurant and restaurant.owner_id == current_user.id:
            return order

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this order."
        )
        # =====================================================
    # Customer Order History
    # =====================================================

    def get_customer_orders(
        self,
        db: Session,
        current_user: User
    ):

        return self.order_repository.get_orders_by_customer(
            db,
            current_user.id
        )
        # =====================================================
    # Restaurant Orders
    # =====================================================

    def get_restaurant_orders(
        self,
        db: Session,
        restaurant_id: int,
        current_user: User
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

        if restaurant.owner_id != current_user.id:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized."
            )

        return self.order_repository.get_orders_by_restaurant(
            db,
            restaurant_id
        )
        # =====================================================
    # Update Order Status
    # =====================================================

    def update_order_status(
        self,
        db: Session,
        order_id: int,
        status_value: str,
        current_user: User
    ):
        order = self.order_repository.get_order_by_id(
            db,
            order_id
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )

        restaurant = self.restaurant_repository.get_restaurant_by_id(
            db,
            order.restaurant_id
        )

        if restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update this order."
            )

        allowed_statuses = [
            "PLACED",
            "ACCEPTED",
            "PREPARING",
            "READY",
            "DELIVERED",
            "CANCELLED"
        ]

        if status_value not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status."
            )

        valid_transitions = {
            "PLACED": [
                "ACCEPTED",
                "CANCELLED"
            ],
            "ACCEPTED": [
                "PREPARING",
                "CANCELLED"
            ],
            "PREPARING": [
                "READY"
            ],
            "READY": [
                "DELIVERED"
            ],
            "DELIVERED": [],
            "CANCELLED": []
        }

        if status_value not in valid_transitions[order.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot change order "
                    f"from {order.status} "
                    f"to {status_value}."
                )
            )

        order.status = status_value

        self.order_repository.update_order(
            db,
            order
        )

        db.commit()

        db.refresh(order)

        return order