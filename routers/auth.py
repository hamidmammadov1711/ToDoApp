"""Bu modul istifadəçi qeydiyyatı və giriş üçün API endpoint-lərini təmin edir. İki əsas endpoint var:
1. POST /auth/ - Yeni istifadəçi yaratmaq üçün istifadə olunur. İstifadəçi məlumatları (username, email, first_name, last_name, password, role) qəbul edir və verilənlər bazasına yeni bir istifadəçi əlavə edir.
2. POST /auth/token - İstifadəçi girişini təmin etmək üçün istifadə olunur. İstifadəçi adı və şifrə qəbul edir, istifadəçi doğrulamasını həyata keçirir və uğurluqdan sonra JWT tokeni qaytarır. Bu token, istifadəçinin kimliyini təsdiqlamaq və digər endpoint-lərə giriş üçün istifadə olunur."""
from datetime import timedelta, datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from starlette import status

# dependencies.py-dən SECRET_KEY, ALGORITHM və digərlərini import edirik
from dependencies import (
    db_dependency,
    authenticate_user,
    bcrypt_context,
    SECRET_KEY,
    ALGORITHM
)
from models import Users

router = APIRouter(
    prefix='/auth',
    tags=['🔐 auth']
)


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """

    :param db:
    :param create_user_request:
    :return:
    """
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=create_user_request.role
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    """

    :param form_data:
    :param db:
    :return:
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    # expires_delta-nı düzgün ötürün
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """

    :param username:
    :param user_id:
    :param expires_delta:
    :return:
    """
    encode: dict[str, Any] = {"sub": username, "user_id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
