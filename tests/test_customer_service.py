import pytest
from unittest.mock import AsyncMock
from src.modules.customer.service import CustomerService
from src.modules.customer.schemas import CustomerOrderQueryParams
from src.core.error.exceptions import ValidationException


class TestCustomerService:
    
    @pytest.mark.asyncio
    async def test_customers_list_success(self, customer_service, mock_customer_repository):
        # Arrange
        expected_customers = [{"id": "123", "name": "John"}]
        mock_customer_repository.customers_list.return_value = expected_customers
        
        # Act
        result = await customer_service.customers_list()
        
        # Assert
        assert result == expected_customers
        mock_customer_repository.customers_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_customers_orders_success(self, customer_service, mock_customer_repository, sample_customer):
        # Arrange
        query = CustomerOrderQueryParams(email="john@example.com")
        expected_orders = [{"id": "ORDER1", "status": "pending"}]
        
        mock_customer_repository.get_customers.return_value = sample_customer
        mock_customer_repository.customers_orders.return_value = expected_orders
        
        # Act
        result = await customer_service.customers_orders(query)
        
        # Assert
        assert result["id"] == sample_customer.id
        assert result["orders"] == expected_orders
        mock_customer_repository.get_customers.assert_called_once_with(query=query)
        mock_customer_repository.customers_orders.assert_called_once_with(customer_id=sample_customer.id)

    @pytest.mark.asyncio
    async def test_customers_orders_customer_not_found(self, customer_service, mock_customer_repository):
        # Arrange
        query = CustomerOrderQueryParams(email="nonexistent@example.com")
        mock_customer_repository.get_customers.return_value = None
        
        # Act & Assert
        with pytest.raises(ValidationException, match="This Phone number Customer does not exist"):
            await customer_service.customers_orders(query)