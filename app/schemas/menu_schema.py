from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# ======================================================
# Create Menu Item Request
# ======================================================

class MenuItemCreate(BaseModel):

    category_id: int = Field(
        ...,
        gt=0,
        description="Category ID"
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Food Item Name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Food Description"
    )

    price: float = Field(
        ...,
        gt=0,
        description="Food Price"
    )

    preparation_time: int = Field(
        default=15,
        ge=1,
        le=180,
        description="Preparation Time in Minutes"
    )

    image_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Food Image URL"
    )

    is_available: bool = Field(
        default=True,
        description="Availability Status"
    )


# ======================================================
# Update Menu Item Request
# ======================================================

class MenuItemUpdate(BaseModel):

    category_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    price: Optional[float] = Field(
        default=None,
        gt=0
    )

    preparation_time: Optional[int] = Field(
        default=None,
        ge=1,
        le=180
    )

    image_url: Optional[str] = Field(
        default=None,
        max_length=500
    )

    is_available: Optional[bool] = None


# ======================================================
# Menu Item Response
# ======================================================

class MenuItemResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    restaurant_id: int

    category_id: int

    name: str

    description: Optional[str]

    price: float

    preparation_time: int

    image_url: Optional[str]

    is_available: bool

    created_at: datetime

    updated_at: datetime