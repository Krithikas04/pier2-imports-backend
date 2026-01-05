import pytest
from unittest.mock import AsyncMock
from src.modules.orders.service import OrderService


class TestOrderService:
    
    @pytest.mark.asyncio
    async def test_list_orders_success(self, order_service, mock_order_repository):
        # Arrange
        expected_orders = [
            {
                "id": "ORDER1A",
                "status": "pending",
                "order_type": "online",
                "billing_address": {"city": "New York"},
                "items": [{"product_name": "Sofa"}]
            }
        ]
        mock_order_repository.list_all.return_value = expected_orders
        
        # Act
        result = await order_service.list_orders()
        
        # Assert
        assert result == expected_orders
        mock_order_repository.list_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_orders_by_billing_zip_ascending(self, order_service, mock_order_repository):
        # Arrange
        expected_data = [
            {"zip_code": "10001", "total_orders": 5},
            {"zip_code": "10002", "total_orders": 10}
        ]
        mock_order_repository.orders_by_billing_zip.return_value = expected_data
        
        # Act
        result = await order_service.orders_by_billing_zip("asc")
        
        # Assert
        assert result == expected_data
        mock_order_repository.orders_by_billing_zip.assert_called_once_with(order_by="asc")

    @pytest.mark.asyncio
    async def test_in_store_peak_hours(self, order_service, mock_order_repository):
        # Arrange
        expected_data = [
            {"hour": 14, "count": 25},
            {"hour": 15, "count": 22}
        ]
        mock_order_repository.in_store_peak_hours.return_value = expected_data
        
        # Act
        result = await order_service.in_store_peak_hours()
        
        # Assert
        assert result == expected_data
        mock_order_repository.in_store_peak_hours.assert_called_once()