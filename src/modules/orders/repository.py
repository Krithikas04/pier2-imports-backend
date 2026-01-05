from collections.abc import Callable
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.modules.orders.models import Orders


class OrderRepository:
    def __init__(self, session_factory: Callable[[], AsyncSession], model: Type = Orders) -> None:
        self.session_factory = session_factory
        self.model = model

    # List all orders
    async def list_all(self) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text("""
                SELECT
                    o.id,
                    o.status,
                    o.order_type,
                    json_build_object(
                        'id', ba.id,
                        'address_label', ba.address_label,
                        'street', ba.street,
                        'city', ba.city,
                        'state', ba.state,
                        'zip_code', ba.zip_code
                    ) AS billing_address,
                    json_agg(
                        json_build_object(
                            'product_name', oi.product_name,
                            'quantity', oi.quantity,
                            'shipping_address', json_build_object(
                                'id', sa.id,
                                'address_label', sa.address_label,
                                'street', sa.street,
                                'city', sa.city,
                                'state', sa.state,
                                'zip_code', sa.zip_code
                            )
                        )
                    ) AS items
                FROM orders o
                JOIN addresses ba ON o.billing_address_id = ba.id
                JOIN order_items oi ON o.id = oi.order_id
                JOIN addresses sa ON oi.shipping_address_id = sa.id
                GROUP BY o.id, ba.id;
            """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows
    
    async def orders_by_billing_zip(self, order_by: str) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text(f"""
                    SELECT
                        zip_code,
                        COUNT(*) AS total_orders
                    FROM orders
                    JOIN addresses ON orders.billing_address_id = addresses.id
                    GROUP BY zip_code
                    ORDER BY total_orders {order_by};
                """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows
        
    async def orders_by_shipping_zip(self, order_by: str) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text(f"""
                    SELECT
                        sa.zip_code,
                        COUNT(*) AS total_orders
                    FROM orders o
                    JOIN order_items oi ON o.id = oi.order_id
                    JOIN addresses sa ON oi.shipping_address_id = sa.id
                    GROUP BY sa.zip_code
                    ORDER BY total_orders {order_by};
                """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows
        
    async def in_store_peak_hours(self) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text("""
                    SELECT EXTRACT(HOUR FROM created_at) AS hour, COUNT(*)
                    FROM orders
                    WHERE order_type = 'in_store'
                    GROUP BY hour
                    ORDER BY COUNT(*) DESC;
                """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows
        
    async def top_instore_customers(self) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text("""
                    SELECT
                        o.customer_id,
                        c.phone,
                        COUNT(*) AS total_orders
                    FROM orders o
                    JOIN customers c ON o.customer_id = c.id
                    WHERE o.order_type = 'in_store'
                    GROUP BY o.customer_id, c.phone
                    ORDER BY total_orders DESC
                    LIMIT 5;
                """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows