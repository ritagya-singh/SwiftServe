from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.current_user import get_current_user

from app.models.user import User

from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

service = CategoryService()


# ==========================================================
# Create Category
# ==========================================================

@router.post(
    "/restaurant/{restaurant_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    restaurant_id: int,
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.create_category(
        db=db,
        restaurant_id=restaurant_id,
        current_user=current_user,
        request=request
    )


# ==========================================================
# Get All Categories Of A Restaurant
# ==========================================================

@router.get(
    "/restaurant/{restaurant_id}",
    response_model=List[CategoryResponse]
)
def get_categories(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    return service.get_categories(
        db=db,
        restaurant_id=restaurant_id
    )


# ==========================================================
# Get Category By ID
# ==========================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    return service.get_category(
        db=db,
        category_id=category_id
    )


# ==========================================================
# Update Category
# ==========================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.update_category(
        db=db,
        category_id=category_id,
        current_user=current_user,
        request=request
    )


# ==========================================================
# Delete Category
# ==========================================================

@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.delete_category(
        db=db,
        category_id=category_id,
        current_user=current_user
    )