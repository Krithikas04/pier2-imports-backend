from collections.abc import Callable
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload
from src.modules.customer.models import Customers, Address
from src.modules.customer.schemas import CustomerOrderQueryParams


class CustomerRepository:
    def __init__(self, session_factory: Callable[[], AsyncSession], model: Type = Customers) -> None:
        self.session_factory = session_factory
        self.model = model



    async def get_customers(self, query: CustomerOrderQueryParams) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = select(self.model)
            if query.phone:
                stmt = stmt.where(self.model.phone == query.phone)
            if query.email:
                stmt = stmt.where(self.model.email == query.email)
            result = await session.execute(stmt)
            customer = result.scalars().one_or_none()
            return customer

    # List all customers
    async def customers_list(self) -> None:
        async with self.session_factory() as session:  # use session_factory
            stmt = text("""
                SELECT
                    c.id,
                    c.first_name,
                    c.last_name,
                    c.phone,
                    c.email,

                    json_agg(
                        json_build_object(
                            'id', a.id,
                            'address_type', a.address_type,
                            'street', a.street,
                            'city', a.city,
                            'state', a.state,
                            'zip_code', a.zip_code
                        )
                    ) FILTER (WHERE a.address_type = 'billing') AS billing_addresses,
                        
                    json_agg(
                        json_build_object(
                            'id', a.id,
                            'address_type', a.address_type,
                            'street', a.street,
                            'city', a.city,
                            'state', a.state,
                            'zip_code', a.zip_code
                        )
                    ) FILTER (WHERE a.address_type = 'shipping') AS shipping_addresses
                        
                FROM customers c
                LEFT JOIN addresses a ON c.id = a.customer_id
                GROUP BY c.id;
            """)

            result = await session.execute(stmt)
            rows = result.mappings().all()
            return rows

    # List customers all orders
    async def customers_orders(self, customer_id:str) -> None:
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
                WHERE o.customer_id = :customer_id
                GROUP BY o.id, ba.id;
            """)

            result = await session.execute(stmt, {"customer_id": customer_id})
            rows = result.mappings().all()
            return rows