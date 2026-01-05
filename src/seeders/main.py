# pylint: skip-file

import asyncio

from sqlalchemy import text
from src.config import settings
from src.core.db import Base, Database
from src.core.error.exceptions import DatabaseError
from src.modules.customer.models import Customers  # noqa
from src.seeders.customer import seed_customer_data
from src.seeders.order import seed_order_data
from src.modules.orders.models import Orders, OrderItems  # noqa


class SeedDatabase(Database):
    async def drop_database(self) -> None:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            result = await connection.execute(
                text(
                    """SELECT
                        convert_from(tablename::bytea, 'UTF8') as tablename
                    FROM
                        pg_tables
                    WHERE
                        schemaname = 'public';
                    """
                )
            )
            tables = [row[0] for row in result.fetchall()]
            # Drop each table with CASCADE
            for table in tables:
                await connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))

    async def create_database(self) -> None:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)


async def seed_all_tables(db: SeedDatabase) -> None:
    async with db.session() as session:
        await seed_customer_data(session=session)
        await seed_order_data(session=session)
        await session.commit()


async def main() -> None:
    db = SeedDatabase(db_url=settings.DATABASE_URL)
    await db.drop_database()
    await db.create_database()
    await seed_all_tables(db=db)
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
