import random
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.orders.models import Orders, OrderItems


async def seed_order_data(session: AsyncSession) -> None:
    order_data = []
    order_items_data = []

    for i in range(1, 10):
        num_orders = random.randint(1, 9)
        customer_id = f"01H195V483BK2BQXJBV0HXY8{num_orders}R"
        billing_address_id = f"01H195V483BK2BQXJBV0HXY8{i}A"
        shipping_address_id = f"01H195V483BK2BQXJBV0HXY8{i}B"

        # Online order
        order_id_online = f"ORDER{i}A"
        order_data.append(
            Orders(
                id=order_id_online,
                customer_id=customer_id,
                billing_address_id=billing_address_id,
                order_type="online",
                status="pending",
            )
        )

        # Add order items for online order
        order_items_data.extend([
            OrderItems(
                id=f"ITEM{i}A1",
                order_id=order_id_online,
                product_name="Sofa",
                quantity=1,
                shipping_address_id=shipping_address_id
            ),
            OrderItems(
                id=f"ITEM{i}A2",
                order_id=order_id_online,
                product_name="Table",
                quantity=1,
                shipping_address_id=billing_address_id  # Different shipping address
            )
        ])

        # In-store order
        order_id_instore = f"ORDER{i}B"
        order_data.append(
            Orders(
                id=order_id_instore,
                customer_id=customer_id,
                billing_address_id=billing_address_id,
                order_type="in_store",
                status="pending",
            )
        )

        # Add order items for in-store order
        order_items_data.append(
            OrderItems(
                id=f"ITEM{i}B1",
                order_id=order_id_instore,
                product_name="Chair",
                quantity=2,
                shipping_address_id=shipping_address_id
            )
        )

    session.add_all(order_data)
    await session.commit()  # Commit orders first
    
    session.add_all(order_items_data)
    await session.commit()  # Then commit order items
