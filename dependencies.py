"""This module contains functions and dependencies used to manage user authentication
 and database sessions in a FastAPI application."""
import json
import os
from pathlib import Path
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import session_local
from models import Users

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-tests")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    """Creates a database session."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: Session):
    """Authentication with username and password."""
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not bcrypt_context.verify(password, str(user.hashed_password)):
        return False
    return user


# ==================== 1. FOR API ENDPOINTS (admin.py, users.py) ====================

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    For API endpoints: Reads token from Authorization header.
    Throws exception if token is invalid (401).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")

        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")


# Type alias for API endpoints (admin.py, users.py refer to this)
user_dependency = Annotated[dict, Depends(get_current_user)]


# ==================== 2. FOR WEB PAGES (todos.py) ====================

async def get_current_user_from_cookie(request: Request) -> Optional[dict]:
    """
    For web pages: Reads token from cookie.
    It DOES NOT throw an Exception, but instead returns None (to redirect).
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            return None

        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        return None


# ==================== 3. i18n (TRANSLATE) COMPATIBILITY ====================

LOCALES_DIR = Path(__file__).parent / "locales"
TRANSLATIONS = {}

for _lang in ["en", "az"]:
    locale_file = LOCALES_DIR / f"{_lang}.json"
    if locale_file.exists():
        with open(locale_file, "r", encoding="utf-8") as f:
            TRANSLATIONS[_lang] = json.load(f)
    else:
        TRANSLATIONS[_lang] = {}


def get_translations_from_cookie(request: Request) -> dict:
    """
    Reads "lang" from cookie, sets it to "az" if not present.
    Returns the corresponding translation dictionary.
    """
    lang = request.cookies.get("lang", "az")
    if lang not in TRANSLATIONS:
        lang = "az"
    return TRANSLATIONS[lang]
