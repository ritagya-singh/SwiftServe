from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# ======================================================
# Create Inventory Item Request
# ======================================================

class InventoryItemCreate(BaseModel):

    ingredient_name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Ingredient Name"
    )

    unit: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Measurement Unit"
    )

    quantity: float = Field(
        ...,
        ge=0,
        description="Current Quantity"
    )

    minimum_quantity: float = Field(
        default=5,
        ge=0,
        description="Minimum Stock Quantity"
    )

    is_active: bool = Field(
        default=True,
        description="Inventory Status"
    )


# ======================================================
# Update Inventory Item Request
# ======================================================

class InventoryItemUpdate(BaseModel):

    ingredient_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    unit: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20
    )

    quantity: Optional[float] = Field(
        default=None,
        ge=0
    )

    minimum_quantity: Optional[float] = Field(
        default=None,
        ge=0
    )

    is_active: Optional[bool] = None


# ======================================================
# Inventory Item Response
# ======================================================

class InventoryItemResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    restaurant_id: int

    ingredient_name: str

    unit: str

    quantity: float

    minimum_quantity: float

    is_active: bool

    created_at: datetime

    updated_at: datetime