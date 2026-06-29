from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


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
# Create Payment Request
# =====================================================

class PaymentCreate(BaseModel):

    payment_method: PaymentMethod = Field(
        ...,
        description="Selected Payment Method"
    )


# =====================================================
# Update Payment Status Request
# =====================================================

class PaymentStatusUpdate(BaseModel):

    payment_status: PaymentStatus = Field(
        ...,
        description="Updated Payment Status"
    )


# =====================================================
# Payment Response
# =====================================================

class PaymentResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    order_id: int

    customer_id: int

    amount: float

    payment_method: PaymentMethod

    payment_status: PaymentStatus

    transaction_id: Optional[str]

    paid_at: Optional[datetime]

    created_at: datetime

    updated_at: datetime