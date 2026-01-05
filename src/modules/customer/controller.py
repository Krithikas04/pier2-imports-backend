from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from src.modules.customer.schemas import CustomerOrderQueryParams
from src.modules.customer.service import CustomerService
from src.core.di import Container

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=None)
@inject
async def customers_list(
    request: Request,
    customer_service: CustomerService = Depends(Provide[Container.customer_service]),
):
    return await customer_service.customers_list()


@router.get("/orders", response_model=None)
@inject
async def customers_orders(
    request: Request,
    query: CustomerOrderQueryParams = Depends(),
    customer_service: CustomerService = Depends(Provide[Container.customer_service]),
):
    return await customer_service.customers_orders(query=query)