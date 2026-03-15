"""Bu modul, FastAPI tətbiqində istifadəçi autentifikasiyası və verilənlər bazası sessiyasını idarə etmək üçün istifadə olunan funksiyaları və asılılıqları ehtiva edir. Burada, istifadəçi məlumatlarını doğrulamaq, tokenləri yoxlamaq və verilənlər bazası ilə əlaqə yaratmaq üçün lazımlı funksiyalar və asılılıqlar təyin edilir. Bu modul, tətbiqin digər hissələrində istifadə edilərək, kodun təkrarını azaltmağa və tətbiqin strukturunu daha təmiz etməyə kömək edir."""

import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import session_local
from models import Users

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=True)


def get_db():
    """
    get_db funksiyası, SQLAlchemy sessiyasını yaratmaq və idarə etmək üçün istifadə olunur. Bu funksiya, FastAPI-nin Depends funksiyası ilə birlikdə istifadə edilərək, hər bir API endpointində verilənlər bazası sessiyasını təmin edir. Sessiya yaradıldıqdan sonra, bu sessiya yield edilir və endpoint işlədikdən sonra sessiya avtomatik olaraq bağlanır.
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# authenticate_user funksiyasını bura köçürürük ki, həm auth.py, həm də digər yerlərdə istifadə edə bilək
def authenticate_user(username: str, password: str, db: Session):
    """
    :param username:
    :param password:
    :param db:
    :return:
    """
    user = db.query(Users).filter(Users.username == username).first()

    if not user or not bcrypt_context.verify(password, str(user.hashed_password)):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)],
                     db: Session = Depends(get_db)):
    """

    :param token:
    :param db:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")  # auth.py-də 'user_id' olaraq qeyd etmisiniz
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")

        # Query daxilində həm ID-ni, həm də ROL-u yoxlayırıq
        user = db.query(Users).filter(Users.id == user_id) \
            .filter(Users.role == user_role).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found or role mismatch")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")


user_dependency = Annotated[Users, Depends(get_current_user)]
