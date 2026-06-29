from fastapi import FastAPI

from app.database import engine
from app.database import Base

from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.menu_item import MenuItem
from app.models.inventory_item import InventoryItem
from app.models.recipe_item import RecipeItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment

from app.routers.auth_router import router as auth_router
from app.routers.restaurant_router import router as restaurant_router
from app.routers.category_router import router as category_router
from app.routers.menu_router import router as menu_router
from app.routers.inventory_router import router as inventory_router
from app.routers.recipe_router import router as recipe_router
from app.routers.order_router import router as order_router
from app.routers.payment_router import router as payment_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SwiftServe API")

app.include_router(auth_router)

app.include_router(restaurant_router)

app.include_router(category_router)

app.include_router(menu_router)

app.include_router(inventory_router)

app.include_router(recipe_router)

app.include_router(order_router)

app.include_router(payment_router)