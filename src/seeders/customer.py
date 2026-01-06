import random
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.customer.models import Customers, Address


async def seed_customer_data(session: AsyncSession) -> None:

    user_data = [
        Customers(
            id=f"01H195V483BK2BQXJBV0HXY8{i}R",
            first_name=f"First{i}",
            last_name=f"Last{i}",
            phone=f"017100000{i}",
            email=f"user{i}@example.com",
        )
        for i in range(1, 10)
    ]


    session.add_all(user_data)

    await session.commit()

    address_data = [
        Address(
            id=f"01H195V483BK2BQXJBV0HXY8{i}A",
            customer_id=f"01H195V483BK2BQXJBV0HXY8{i}R",
            address_type="billing",
            address_label="home",
            street="1600 Amphitheatre Parkway",
            city="Mountain View",
            state="CA",
            zip_code=f"9404{random.randint(1, 9)}"
        )
        for i in range(1, 10)
    ] + [
        Address(
            id=f"01H195V483BK2BQXJBV0HXY8{i}B",
            customer_id=f"01H195V483BK2BQXJBV0HXY8{i}R",
            address_type="shipping",
            address_label="office",
            street="742 Evergreen Terrace",
            city="New York",
            state="NY",
            zip_code=f"1000{random.randint(1, 9)}"
        )
        for i in range(1, 10)
    ]
    session.add_all(address_data)
