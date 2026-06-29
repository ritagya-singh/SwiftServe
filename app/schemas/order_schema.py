from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


# =====================================================
# Order Item Create
# =====================================================

class OrderItemCreate(BaseModel):

    menu_item_id: int

    quantity: int = Field(
        gt=0,
        description="Quantity must be greater than zero."
    )


# =====================================================
# Order Create
# =====================================================

class OrderCreate(BaseModel):

    restaurant_id: int

    items: List[OrderItemCreate]


# =====================================================
# Order Status Update
# =====================================================

class OrderStatusUpdate(BaseModel):

    status: str


# =====================================================
# Order Item Response
# =====================================================

class OrderItemResponse(BaseModel):

    id: int

    order_id: int

    menu_item_id: int

    quantity: int

    unit_price: float

    total_price: float

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================================
# Order Response
# =====================================================

class OrderResponse(BaseModel):

    id: int

    restaurant_id: int

    customer_id: int

    total_amount: float

    status: str

    created_at: datetime

    updated_at: datetime

    order_items: List[OrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )