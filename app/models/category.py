from datetime import datetime
from datetime import timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):

    __tablename__ = "categories"

    # ===================================
    # Primary Key
    # ===================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ===================================
    # Foreign Key
    # ===================================

    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # ===================================
    # Category Name
    # ===================================

    name = Column(
        String(100),
        nullable=False
    )

    # ===================================
    # Description
    # ===================================

    description = Column(
        String(300),
        nullable=True
    )

    # ===================================
    # Timestamps
    # ===================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ===================================
    # Relationships
    # ===================================

    restaurant = relationship(
        "Restaurant",
        back_populates="categories"
    )

    menu_items = relationship(
        "MenuItem",
        back_populates="category",
        cascade="all, delete-orphan"
    )