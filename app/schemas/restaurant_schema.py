from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================
# Create Restaurant Request
# ==========================
class RestaurantCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr

    address: str = Field(..., min_length=5, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    pincode: str = Field(..., min_length=6, max_length=10)

    opening_time: str
    closing_time: str


# ==========================
# Update Restaurant Request
# ==========================
class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    email: Optional[EmailStr] = None

    address: Optional[str] = Field(default=None, min_length=5, max_length=255)
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    state: Optional[str] = Field(default=None, min_length=2, max_length=100)
    pincode: Optional[str] = Field(default=None, min_length=6, max_length=10)

    opening_time: Optional[str] = None
    closing_time: Optional[str] = None

    is_open: Optional[bool] = None


# ==========================
# Restaurant Response
# ==========================
class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str
    description: Optional[str]

    owner_id: int

    phone: str
    email: EmailStr

    address: str
    city: str
    state: str
    pincode: str

    opening_time: str
    closing_time: str

    is_open: bool

    created_at: datetime
    updated_at: datetime