# Pier 2 Imports Backend System

A Python-based backend system for Pier 2 Imports, managing customers, orders, billing & shipping addresses, and analytics for home and office goods operations. Supports both warehouse shipping and retail showroom purchases with CLI and API interfaces.

## Features

* Home and office goods order management (online delivery & in-store pickup)
* CRM with duplicate prevention (email/phone based)
* Multiple shipping addresses per order (homes, offices, furniture delivery)
* Business analytics and intelligence
* Command-line interface for operations
* REST API for integrations

## Tech Stack
* **Python 3.12** - Core language
* **PostgreSQL** - Database 
* **SQLAlchemy** - ORM for database operations
* **FastAPI** - Web API framework
* **Click** - CLI framework
* **Pydantic** - Data validation

## Quick Start

### 1. Setup Environment
```bash
# Clone repository
git clone https://github.com/Krithikas04/pier2-imports-backend.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Install PostgreSQL
brew install postgresql@14  # macOS
sudo apt-get install postgresql-14  # Ubuntu

# Start PostgreSQL
brew services start postgresql@14  # macOS
sudo systemctl start postgresql  # Ubuntu

# Create database and user
createuser -s your_username
createdb pier2_imports_db
```

### 3. Configuration
Create `.env` file:
```env
APP_VERSION=v1
DEBUG=True
APP_ENV=dev
DATABASE_URL=postgresql+psycopg://your_username:password@localhost:5432/pier2_imports_db
```

### 4. Initialize Database
```bash
# Seed initial data
python3 -m src.seeders.main
```

## Usage Examples

### Command Line Interface

#### List all customers
```bash
python cli.py list-customers
```

#### Get customer order history
```bash
# By email
python cli.py get-customer-orders --email user1@example.com

# By phone
python cli.py get-customer-orders --phone 0171000001
```

#### Analytics commands
```bash
# Orders by billing ZIP (descending)
python cli.py billing-zip-analytics --order-by desc

# Orders by shipping ZIP (ascending)
python cli.py shipping-zip-analytics --order-by asc

# Peak hours for in-store purchases
python cli.py peak-hours

# Top customers by in-store orders
python cli.py top-customers
```

#### List all orders
```bash
python cli.py list-orders
```

### Web API Interface

#### Start API server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

#### API endpoints
- **GET** `/api/v1/customers/` - List customers
- **GET** `/api/v1/customers/orders?email=X&phone=Y` - Customer orders
- **GET** `/api/v1/orders/` - List orders
- **GET** `/api/v1/orders/billing-zip?order_by=asc` - Billing ZIP analytics
- **GET** `/api/v1/orders/shipping-zip?order_by=desc` - Shipping ZIP analytics
- **GET** `/api/v1/orders/in-store/peak-hours` - Peak hours
- **GET** `/api/v1/orders/top-instore-customers` - Top customers

#### Interactive API docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Run unit tests
```bash
# All tests
python -m pytest tests/ -v

# Specific test files
python -m pytest tests/test_validation.py -v
python -m pytest tests/test_customer_service.py -v
```

### Test CLI commands
```bash
# Test customer lookup
python cli.py get-customer-orders --email user1@example.com

# Test analytics
python cli.py billing-zip-analytics --order-by desc
```

## Project Structure
```
pier2-imports-backend/
├── cli.py                 # Command-line interface
├── src/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration
│   ├── routers.py        # API routes
│   ├── core/             # Core utilities
│   ├── modules/          # Business modules
│   └── seeders/          # Database seeders
├── tests/                # Unit tests
├── requirements.txt      # Dependencies
├── pytest.ini          # Test configuration
└── README.md            # This file
```

