from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# ============================================
# Create Category Request
# ============================================

class CategoryCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=300,
        description="Category description"
    )


# ============================================
# Update Category Request
# ============================================

class CategoryUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=300
    )


# ============================================
# Category Response
# ============================================

class CategoryResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    restaurant_id: int

    name: str

    description: Optional[str]

    created_at: datetime

    updated_at: datetime