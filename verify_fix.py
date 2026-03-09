import os
import sys

# Change to the project directory
os.chdir('D:\\ToDoApp')
sys.path.insert(0, 'D:\\ToDoApp')

print("Python version:", sys.version)
print("\nTesting imports step by step...\n")

try:
    print("Step 1: Import database")
    import database

    print("✓ Success\n")

    print("Step 2: Import models")
    import models

    print("✓ Success\n")

    print("Step 3: Import dependencies")
    import dependencies

    print("✓ Success")
    print(f"  - bcrypt_context exists: {hasattr(dependencies, 'bcrypt_context')}\n")

    print("Step 4: Import routers.auth")
    from routers import auth

    print("✓ Success")
    print(f"  - router exists: {hasattr(auth, 'router')}")
    print(f"  - Using bcrypt_context: {auth.bcrypt_context is dependencies.bcrypt_context}\n")

    print("Step 5: Import routers.todos")
    from routers import todos

    print("✓ Success\n")

    print("Step 6: Import main")
    import main

    print("✓ Success")
    print(f"  - app exists: {hasattr(main, 'app')}\n")

    print("\n" + "=" * 60)
    print("✓✓✓ ALL IMPORTS SUCCESSFUL - CIRCULAR IMPORT FIXED! ✓✓✓")
    print("=" * 60)

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
