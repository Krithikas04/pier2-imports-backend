from sqlalchemy import TIMESTAMP, String, func, ForeignKey, Enum, Integer
from src.core.db.connector import Base
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID
from datetime import datetime


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )
    customer_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("customers.id"), nullable=False
    )
    billing_address_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("addresses.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(Enum("pending", "shipped", "delivered", "canceled", name="order_status_enum"), default="pending", nullable=False)
    order_type: Mapped[str] = mapped_column(Enum("online", "in_store", name="order_type_enum"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )


class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )
    order_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("orders.id"), nullable=False
    )
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    shipping_address_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("addresses.id"), nullable=False
    )
