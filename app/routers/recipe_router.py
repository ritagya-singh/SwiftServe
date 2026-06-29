from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.current_user import get_current_user

from app.models.user import User

from app.schemas.recipe_schema import (
    RecipeItemCreate,
    RecipeItemUpdate,
    RecipeItemResponse
)

from app.services.recipe_service import RecipeService

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

service = RecipeService()


# =====================================================
# Create Recipe Item
# =====================================================

@router.post(
    "/menu/{menu_item_id}",
    response_model=RecipeItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_recipe_item(
    menu_item_id: int,
    request: RecipeItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.create_recipe_item(
        db=db,
        menu_item_id=menu_item_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Get Recipe Item By ID
# =====================================================

@router.get(
    "/{recipe_item_id}",
    response_model=RecipeItemResponse
)
def get_recipe_item(
    recipe_item_id: int,
    db: Session = Depends(get_db)
):

    return service.get_recipe_item(
        db=db,
        recipe_item_id=recipe_item_id
    )


# =====================================================
# Get Recipe Of Menu Item
# =====================================================

@router.get(
    "/menu/{menu_item_id}",
    response_model=List[RecipeItemResponse]
)
def get_recipe_items_by_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db)
):

    return service.get_recipe_items_by_menu_item(
        db=db,
        menu_item_id=menu_item_id
    )


# =====================================================
# Update Recipe Item
# =====================================================

@router.put(
    "/{recipe_item_id}",
    response_model=RecipeItemResponse
)
def update_recipe_item(
    recipe_item_id: int,
    request: RecipeItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.update_recipe_item(
        db=db,
        recipe_item_id=recipe_item_id,
        current_user=current_user,
        request=request
    )


# =====================================================
# Delete Recipe Item
# =====================================================

@router.delete(
    "/{recipe_item_id}"
)
def delete_recipe_item(
    recipe_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return service.delete_recipe_item(
        db=db,
        recipe_item_id=recipe_item_id,
        current_user=current_user
    )