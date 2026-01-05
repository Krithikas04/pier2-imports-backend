#!/usr/bin/env python3
"""
Pier 2 Imports Order Management CLI
Command-line interface for managing customers, orders, and analytics.
"""

import asyncio
import click
import json
from typing import Optional
from src.core.db import Database
from src.modules.customer.service import CustomerService
from src.modules.customer.repository import CustomerRepository
from src.modules.orders.service import OrderService
from src.modules.orders.repository import OrderRepository
from src.modules.customer.schemas import CustomerOrderQueryParams
from src.config import settings


class Pier2ImportsCLI:
    def __init__(self):
        self.db = Database(db_url=settings.DATABASE_URL)
        self.customer_service = CustomerService(CustomerRepository(self.db.session))
        self.order_service = OrderService(OrderRepository(self.db.session))

    async def close(self):
        await self.db.close()


@click.group()
def cli():
    """Pier 2 Imports Order Management System CLI"""
    pass


@cli.command()
@click.option('--email', help='Customer email address')
@click.option('--phone', help='Customer phone number')
def get_customer_orders(email: Optional[str], phone: Optional[str]):
    """Get customer order history by email or phone"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            if not email and not phone:
                click.echo("Error: Either email or phone must be provided")
                return
            
            query = CustomerOrderQueryParams(email=email, phone=phone)
            result = await warehouse.customer_service.customers_orders(query)
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
def list_customers():
    """List all customers"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            customers = await warehouse.customer_service.customers_list()
            click.echo(json.dumps(customers, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
def list_orders():
    """List all orders"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            orders = await warehouse.order_service.list_orders()
            click.echo(json.dumps(orders, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
@click.option('--order-by', type=click.Choice(['asc', 'desc']), default='desc', help='Sort order')
def billing_zip_analytics(order_by: str):
    """Show orders analytics by billing ZIP code"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            result = await warehouse.order_service.orders_by_billing_zip(order_by)
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
@click.option('--order-by', type=click.Choice(['asc', 'desc']), default='desc', help='Sort order')
def shipping_zip_analytics(order_by: str):
    """Show orders analytics by shipping ZIP code"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            result = await warehouse.order_service.orders_by_shipping_zip(order_by)
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
def peak_hours():
    """Show peak hours for in-store purchases"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            result = await warehouse.order_service.in_store_peak_hours()
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


@cli.command()
def top_customers():
    """Show top 5 customers with most in-store orders"""
    async def run():
        warehouse = Pier2ImportsCLI()
        try:
            result = await warehouse.order_service.top_instore_customers()
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"Error: {str(e)}")
        finally:
            await warehouse.close()
    
    asyncio.run(run())


if __name__ == '__main__':
    cli()