from datetime import datetime, timezone
datetime.now(timezone.utc)
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # Restaurant
    # =====================================================

    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =====================================================
    # Customer
    # =====================================================

    customer_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =====================================================
    # Order Details
    # =====================================================

    total_amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="PLACED"
    )

    # =====================================================
    # Timestamps
    # =====================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # =====================================================
    # Relationships
    # =====================================================

    restaurant = relationship(
        "Restaurant",
        back_populates="orders"
    )

    customer = relationship(
        "User",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )