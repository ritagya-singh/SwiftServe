from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.current_user import get_current_user

from app.models.user import User

from app.schemas.menu_schema import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)

from app.services.menu_service import MenuService

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

service = MenuService()


# =====================================================
# Create Menu Item
# =====================================================

@router.post(
    "/restaurant/{restaurant_id}",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_menu_item(
    restaurant_id: int,
    request: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.create_menu_item(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Get Menu Item By ID
# =====================================================

@router.get(
    "/{menu_item_id}",
    response_model=MenuItemResponse
)
def get_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db)
):

    return service.get_menu_item(
        db=db,
        menu_item_id=menu_item_id
    )


# =====================================================
# Get Menu Items Of Restaurant
# =====================================================

@router.get(
    "/restaurant/{restaurant_id}",
    response_model=List[MenuItemResponse]
)
def get_menu_items_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    return service.get_menu_items_by_restaurant(
        db=db,
        restaurant_id=restaurant_id
    )


# =====================================================
# Get Menu Items By Category
# =====================================================

@router.get(
    "/category/{category_id}",
    response_model=List[MenuItemResponse]
)
def get_menu_items_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    return service.get_menu_items_by_category(
        db=db,
        category_id=category_id
    )


# =====================================================
# Update Menu Item
# =====================================================

@router.put(
    "/{menu_item_id}",
    response_model=MenuItemResponse
)
def update_menu_item(
    menu_item_id: int,
    request: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.update_menu_item(
        db=db,
        menu_item_id=menu_item_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Delete Menu Item
# =====================================================

@router.delete(
    "/{menu_item_id}"
)
def delete_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.delete_menu_item(
        db=db,
        menu_item_id=menu_item_id,
        current_user=current_user
    )