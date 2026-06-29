from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# =====================================================
# Create Recipe Item Request
# =====================================================

class RecipeItemCreate(BaseModel):

    inventory_item_id: int = Field(
        ...,
        gt=0,
        description="Inventory Item ID"
    )

    quantity_required: float = Field(
        ...,
        gt=0,
        description="Quantity Required"
    )


# =====================================================
# Update Recipe Item Request
# =====================================================

class RecipeItemUpdate(BaseModel):

    inventory_item_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    quantity_required: Optional[float] = Field(
        default=None,
        gt=0
    )


# =====================================================
# Recipe Item Response
# =====================================================

class RecipeItemResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    menu_item_id: int

    inventory_item_id: int

    quantity_required: float

    created_at: datetime

    updated_at: datetime