from dependency_injector import containers, providers

from src.config import settings
from src.core.db.connector import Database
from src.modules.customer.models import Customers
from src.modules.customer.service import CustomerService
from src.modules.customer.repository import CustomerRepository
from src.modules.orders.models import Orders
from src.modules.orders.repository import OrderRepository
from src.modules.orders.service import OrderService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.customer.controller",
            "src.modules.orders.controller",
        ]
    )
    db = providers.Singleton(
        Database,
        db_url=settings.DATABASE_URL,
    )

    customer_repository = providers.Factory(
        CustomerRepository,
        session_factory=db.provided.session,
        model=Customers,
    )

    customer_service = providers.Factory(
        CustomerService,
        repository=customer_repository,
    )


    order_repository = providers.Factory(
        OrderRepository,
        session_factory=db.provided.session,
        model=Orders,
    )

    order_service = providers.Factory(
        OrderService,
        repository=order_repository,
    )

    