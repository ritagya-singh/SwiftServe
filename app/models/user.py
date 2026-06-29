from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    restaurants = relationship(
        "Restaurant",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="customer",
        cascade="all, delete-orphan"
    )