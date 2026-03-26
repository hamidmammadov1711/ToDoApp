from jose import jwt, JWTError

# Conditional parameters for testing
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def test_jwt():
    try:
        print("Testing has begun...")
        # 1. Token yaradaq
        token = jwt.encode({"sub": "testuser"}, SECRET_KEY, algorithm=ALGORITHM)
        print(f"Created Token: {token}")

        # 2. Tokeni deşifrə edək
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token decrypted: {decoded}")

        # 3. Bilərəkdən yanlış imza ilə xəta yaratmağa çalışaq (JWTError testi)
        print("Attempted decryption with incorrect key...")
        jwt.decode(token, "wrongkey", algorithms=[ALGORITHM])

    except JWTError:
        print("✓ Success! JWTError caught (System is working properly).")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_jwt()