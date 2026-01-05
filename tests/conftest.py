import pytest
from unittest.mock import AsyncMock
from src.modules.customer.service import CustomerService
from src.modules.orders.service import OrderService
from src.modules.customer.repository import CustomerRepository
from src.modules.orders.repository import OrderRepository


@pytest.fixture
def mock_customer_repository():
    return AsyncMock(spec=CustomerRepository)


@pytest.fixture
def mock_order_repository():
    return AsyncMock(spec=OrderRepository)


@pytest.fixture
def customer_service(mock_customer_repository):
    return CustomerService(repository=mock_customer_repository)


@pytest.fixture
def order_service(mock_order_repository):
    return OrderService(repository=mock_order_repository)


@pytest.fixture
def sample_customer():
    class MockCustomer:
        id = "01H195V483BK2BQXJBV0HXY81R"
        first_name = "John"
        last_name = "Doe"
        phone = "0171000001"
        email = "john@example.com"
    return MockCustomer()


@pytest.fixture
def sample_orders():
    return [
        {
            "id": "ORDER1A",
            "status": "pending",
            "order_type": "online",
            "billing_address": {"city": "New York"},
            "items": [{"product_name": "Sofa", "shipping_address": {"city": "Brooklyn"}}]
        }
    ]