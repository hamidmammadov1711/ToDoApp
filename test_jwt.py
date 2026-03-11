from jose import jwt, JWTError
import os

# Test üçün şərti parametrlər
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def test_jwt():
    try:
        print("Test başladı...")
        # 1. Token yaradaq
        token = jwt.encode({"sub": "testuser"}, SECRET_KEY, algorithm=ALGORITHM)
        print(f"Token yaradıldı: {token}")

        # 2. Tokeni deşifrə edək
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token deşifrə olundu: {decoded}")

        # 3. Bilərəkdən yanlış imza ilə xəta yaratmağa çalışaq (JWTError testi)
        print("Yanlış açarla deşifrəyə cəhd...")
        jwt.decode(token, "wrongkey", algorithms=[ALGORITHM])

    except JWTError:
        print("✓ Uğurlu! JWTError tutuldu (Sistem düzgün işləyir).")
    except Exception as e:
        print(f"Gözlənilməz xəta: {e}")

if __name__ == "__main__":
    test_jwt()