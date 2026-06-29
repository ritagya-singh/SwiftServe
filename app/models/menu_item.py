from datetime import datetime
from datetime import timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from app.database import Base


class MenuItem(Base):

    __tablename__ = "menu_items"

    # ===================================================
    # Primary Key
    # ===================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ===================================================
    # Foreign Keys
    # ===================================================

    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey(
            "categories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # ===================================================
    # Food Information
    # ===================================================

    name = Column(
        String(150),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    price = Column(
        Float,
        nullable=False
    )

    preparation_time = Column(
        Integer,
        nullable=False,
        default=15
    )

    image_url = Column(
        String(500),
        nullable=True
    )

    is_available = Column(
        Boolean,
        default=True
    )

    # ===================================================
    # Timestamps
    # ===================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ===================================================
    # Relationships
    # ===================================================

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )

    category = relationship(
        "Category",
        back_populates="menu_items"
    )

    recipe_items = relationship(
        "RecipeItem",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )