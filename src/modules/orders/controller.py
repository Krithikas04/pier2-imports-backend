from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Query
from src.modules.orders.service import OrderService
from src.modules.orders.schemas import OrderAnalyticsQueryParams
from src.core.di import Container

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=None)
@inject
async def list_orders(
    request: Request,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.list_orders()


@router.get("/billing-zip", response_model=None)
@inject
async def orders_by_billing_zip(
    request: Request,
    query: OrderAnalyticsQueryParams = Depends(),
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.orders_by_billing_zip(order_by=query.order_by)


@router.get("/shipping-zip", response_model=None)
@inject
async def orders_by_shipping_zip(
    request: Request,
    query: OrderAnalyticsQueryParams = Depends(),
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.orders_by_shipping_zip(order_by=query.order_by)


@router.get("/in-store/peak-hours", response_model=None)
@inject
async def in_store_peak_hours(
    request: Request,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.in_store_peak_hours()


@router.get("/top-instore-customers", response_model=None)
@inject
async def top_instore_customers(
    request: Request,
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.top_instore_customers()