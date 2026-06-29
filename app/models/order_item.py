from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from app.database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # Order
    # =====================================================

    order_id = Column(
        Integer,
        ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =====================================================
    # Menu Item
    # =====================================================

    menu_item_id = Column(
        Integer,
        ForeignKey(
            "menu_items.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =====================================================
    # Quantity
    # =====================================================

    quantity = Column(
        Integer,
        nullable=False
    )

    # =====================================================
    # Pricing
    # =====================================================

    unit_price = Column(
        Float,
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False
    )

    # =====================================================
    # Timestamp
    # =====================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # =====================================================
    # Relationships
    # =====================================================

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="order_items"
    )