from datetime import datetime
from datetime import timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from app.database import Base


class InventoryItem(Base):

    __tablename__ = "inventory_items"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # Restaurant Relationship
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
    # Ingredient Information
    # =====================================================

    ingredient_name = Column(
        String(150),
        nullable=False
    )

    unit = Column(
        String(20),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False,
        default=0
    )

    minimum_quantity = Column(
        Float,
        nullable=False,
        default=5
    )

    is_active = Column(
        Boolean,
        default=True
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
    # Relationship
    # =====================================================

    restaurant = relationship(
        "Restaurant",
        back_populates="inventory_items"
    )

    recipe_items = relationship(
        "RecipeItem",
        back_populates="inventory_item",
        cascade="all, delete-orphan"
    )