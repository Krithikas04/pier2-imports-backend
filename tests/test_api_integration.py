import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestCustomerAPI:
    
    def test_get_customers_list(self, client):
        # Test GET /api/v1/customers/
        response = client.get("/api/v1/customers/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_customer_orders_with_email(self, client):
        # Test GET /api/v1/customers/orders with valid email
        response = client.get("/api/v1/customers/orders?email=user1@example.com")
        # Should return 200 or 400 (if customer not found)
        assert response.status_code in [200, 400]

    def test_get_customer_orders_with_phone(self, client):
        # Test GET /api/v1/customers/orders with valid phone
        response = client.get("/api/v1/customers/orders?phone=0171000001")
        # Should return 200 or 400 (if customer not found)
        assert response.status_code in [200, 400]

    def test_get_customer_orders_missing_params(self, client):
        response = client.get("/api/v1/customers/orders")
        assert response.status_code == 400
        assert "Either phone or email must be provided" in response.json()["message"]

    def test_get_customer_orders_invalid_email(self, client):
        response = client.get("/api/v1/customers/orders?email=invalid-email")
        assert response.status_code == 500  # Pydantic validation error becomes 500


class TestOrdersAPI:
    
    def test_get_orders_list(self, client):
        # Test GET /api/v1/orders/
        response = client.get("/api/v1/orders/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_orders_by_billing_zip_asc(self, client):
        # Test GET /api/v1/orders/billing-zip?order_by=asc
        response = client.get("/api/v1/orders/billing-zip?order_by=asc")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_orders_by_billing_zip_desc(self, client):
        # Test GET /api/v1/orders/billing-zip?order_by=desc
        response = client.get("/api/v1/orders/billing-zip?order_by=desc")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_orders_by_shipping_zip(self, client):
        # Test GET /api/v1/orders/shipping-zip?order_by=asc
        response = client.get("/api/v1/orders/shipping-zip?order_by=asc")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_in_store_peak_hours(self, client):
        # Test GET /api/v1/orders/in-store/peak-hours
        response = client.get("/api/v1/orders/in-store/peak-hours")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_top_instore_customers(self, client):
        # Test GET /api/v1/orders/top-instore-customers
        response = client.get("/api/v1/orders/top-instore-customers")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_billing_zip_missing_order_by(self, client):
        response = client.get("/api/v1/orders/billing-zip")
        assert response.status_code == 400