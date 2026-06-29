from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True
    )

    address = Column(
        String(255),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    state = Column(
        String(100),
        nullable=False
    )

    pincode = Column(
        String(10),
        nullable=False
    )

    opening_time = Column(
        String(10),
        nullable=False
    )

    closing_time = Column(
        String(10),
        nullable=False
    )

    is_open = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="restaurants"
    )
    categories = relationship(
        "Category",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    menu_items = relationship(
        "MenuItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )
    inventory_items = relationship(
        "InventoryItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )
    orders = relationship(
        "Order",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )