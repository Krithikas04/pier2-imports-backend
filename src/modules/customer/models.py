from sqlalchemy import TIMESTAMP, String, func, ForeignKey, Enum
from src.core.db.connector import Base
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID
from datetime import datetime


class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )
    customer_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("customers.id"), nullable=False
    )
    address_type: Mapped[str] = mapped_column(String(30), nullable=True)
    address_label: Mapped[str] = mapped_column(String(30), nullable=True)
    street: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)