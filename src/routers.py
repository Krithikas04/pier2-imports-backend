from fastapi import APIRouter
from src.modules.customer.controller import router as customer_router
from src.modules.orders.controller import router as orders_router

api_router = APIRouter()

api_router.include_router(customer_router)
api_router.include_router(orders_router)
