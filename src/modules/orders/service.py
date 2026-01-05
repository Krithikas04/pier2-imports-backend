from src.modules.orders.repository import OrderRepository

class OrderService:
    def __init__(
        self,
        repository: OrderRepository
    ) -> None:
        self.repository = repository


    async def list_orders(self) -> None:
        return await self.repository.list_all()

    async def orders_by_billing_zip(self, order_by: str) -> None:
        return await self.repository.orders_by_billing_zip(order_by=order_by)

    async def orders_by_shipping_zip(self, order_by: str) -> None:
        return await self.repository.orders_by_shipping_zip(order_by=order_by)

    async def in_store_peak_hours(self) -> None:
        return await self.repository.in_store_peak_hours()
    
    async def top_instore_customers(self) -> None:
        return await self.repository.top_instore_customers()