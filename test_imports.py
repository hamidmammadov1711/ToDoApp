#!/usr/bin/env python3
"""Test script to verify no circular imports exist"""

try:
    print("Testing import chain...")

    print("1. Importing database...")
    import database
    print("   ✓ database imported successfully")

    print("2. Importing models...")
    import models
    print("   ✓ models imported successfully")

    print("3. Importing dependencies...")
    import dependencies
    print("   ✓ dependencies imported successfully")
    print(f"   - bcrypt_context available: {hasattr(dependencies, 'bcrypt_context')}")

    print("4. Importing routers.auth...")
    from routers import auth
    print("   ✓ routers.auth imported successfully")
    print(f"   - Using bcrypt_context from dependencies: {auth.bcrypt_context is dependencies.bcrypt_context}")

    print("5. Importing routers.todos...")
    from routers import todos
    print("   ✓ routers.todos imported successfully")

    print("6. Importing main...")
    import main
    print("   ✓ main imported successfully")

    print("\n✓✓✓ ALL IMPORTS SUCCESSFUL - NO CIRCULAR DEPENDENCY! ✓✓✓")

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

