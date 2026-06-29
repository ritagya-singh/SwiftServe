from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum as SqlEnum
)

from sqlalchemy.orm import relationship

from app.database import Base


# =====================================================
# Payment Method Enum
# =====================================================

class PaymentMethod(str, Enum):

    UPI = "UPI"

    CREDIT_CARD = "CREDIT_CARD"

    DEBIT_CARD = "DEBIT_CARD"

    NET_BANKING = "NET_BANKING"

    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"


# =====================================================
# Payment Status Enum
# =====================================================

class PaymentStatus(str, Enum):

    PENDING = "PENDING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    REFUNDED = "REFUNDED"


# =====================================================
# Payment Model
# =====================================================

class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        SqlEnum(PaymentMethod),
        nullable=False
    )

    payment_status = Column(
        SqlEnum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False
    )

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=True
    )

    paid_at = Column(
        DateTime,
        nullable=True
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

    # ==============================
    # Relationships
    # ==============================

    order = relationship(
        "Order",
        back_populates="payment"
    )

    customer = relationship(
        "User",
        back_populates="payments"
    )