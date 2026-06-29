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


class RecipeItem(Base):

    __tablename__ = "recipe_items"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # Foreign Keys
    # =====================================================

    menu_item_id = Column(
        Integer,
        ForeignKey(
            "menu_items.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    inventory_item_id = Column(
        Integer,
        ForeignKey(
            "inventory_items.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =====================================================
    # Quantity Required
    # =====================================================

    quantity_required = Column(
        Float,
        nullable=False
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

    menu_item = relationship(
        "MenuItem",
        back_populates="recipe_items"
    )

    inventory_item = relationship(
        "InventoryItem",
        back_populates="recipe_items"
    )