#!/usr/bin/env python3
"""
Test script to verify Pier 2 Imports system setup
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.config import settings
    print("✓ Configuration loaded successfully")
    print(f"  Database URL: {settings.DATABASE_URL}")
    print(f"  App Version: {settings.APP_VERSION}")
    print(f"  Environment: {settings.APP_ENV}")
except Exception as e:
    print(f"✗ Configuration failed: {e}")
    sys.exit(1)

try:
    from src.main import app
    print("✓ FastAPI app created successfully")
    print(f"  Title: {app.title}")
    print(f"  Description: {app.description}")
except Exception as e:
    print(f"✗ FastAPI app creation failed: {e}")
    sys.exit(1)

try:
    from cli import Pier2ImportsCLI
    print("✓ CLI class imported successfully")
except Exception as e:
    print(f"✗ CLI import failed: {e}")
    sys.exit(1)

print("\n🎉 Pier 2 Imports Backend System setup verification complete!")
print("Ready to run with the updated branding and database configuration.")