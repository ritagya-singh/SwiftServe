from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.current_user import get_current_user

from app.models.user import User

from app.schemas.inventory_schema import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse
)

from app.services.inventory_service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

service = InventoryService()


# =====================================================
# Create Inventory Item
# =====================================================

@router.post(
    "/restaurant/{restaurant_id}",
    response_model=InventoryItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_inventory_item(
    restaurant_id: int,
    request: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.create_inventory_item(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Get Inventory Item By ID
# =====================================================

@router.get(
    "/{inventory_item_id}",
    response_model=InventoryItemResponse
)
def get_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db)
):

    return service.get_inventory_item(
        db=db,
        inventory_item_id=inventory_item_id
    )


# =====================================================
# Get Inventory Of Restaurant
# =====================================================

@router.get(
    "/restaurant/{restaurant_id}",
    response_model=List[InventoryItemResponse]
)
def get_inventory_items_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    return service.get_inventory_items_by_restaurant(
        db=db,
        restaurant_id=restaurant_id
    )


# =====================================================
# Update Inventory Item
# =====================================================

@router.put(
    "/{inventory_item_id}",
    response_model=InventoryItemResponse
)
def update_inventory_item(
    inventory_item_id: int,
    request: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.update_inventory_item(
        db=db,
        inventory_item_id=inventory_item_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Delete Inventory Item
# =====================================================

@router.delete(
    "/{inventory_item_id}"
)
def delete_inventory_item(
    inventory_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.delete_inventory_item(
        db=db,
        inventory_item_id=inventory_item_id,
        current_user=current_user
    )