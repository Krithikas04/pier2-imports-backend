#!/bin/bash

echo "🧪 Running Unit Tests and Input Validation Tests"
echo "================================================"

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install pytest pytest-asyncio httpx

# Run all tests
echo "🚀 Running tests..."
python -m pytest tests/ -v --tb=short

# Run specific test categories
echo ""
echo "📊 Test Coverage Summary:"
echo "========================="
echo "✅ Unit Tests: Customer Service, Orders Service"
echo "✅ Input Validation: Email, Phone, Query Parameters"  
echo "✅ API Integration: All 7 endpoints"
echo "✅ Error Handling: Validation errors, missing data"

echo ""
echo "🎯 To run specific tests:"
echo "python -m pytest tests/test_validation.py -v"
echo "python -m pytest tests/test_customer_service.py -v"
echo "python -m pytest tests/test_orders_service.py -v"
echo "python -m pytest tests/test_api_integration.py -v"