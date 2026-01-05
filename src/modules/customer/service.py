from src.modules.customer.repository import CustomerRepository
from src.modules.customer.schemas import CustomerOrderQueryParams
from src.core.error.exceptions import ValidationException

class CustomerService:
    def __init__(
        self,
        repository: CustomerRepository
    ) -> None:
        self.repository = repository


    async def customers_list(self) -> None:
        return await self.repository.customers_list()
    

    async def customers_orders(self, query: CustomerOrderQueryParams) -> None:
        customer = await self.repository.get_customers(query=query)
        if not customer:
            raise ValidationException("This Phone number Customer does not exist")
        rows = await self.repository.customers_orders(customer_id=customer.id)

        result = {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone": customer.phone,
                "email": customer.email,
            }
        result["orders"] = rows

        return result