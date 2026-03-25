"""Bu modul istifadəçi qeydiyyatı və giriş üçün API endpoint-lərini təmin edir. İki əsas endpoint var:
1. POST /auth/ - Yeni istifadəçi yaratmaq üçün istifadə olunur.
2. POST /auth/token - İstifadəçi girişini təmin etmək üçün istifadə olunur."""

from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import jwt
from pydantic import BaseModel
from starlette import status

from dependencies import (
    SECRET_KEY, ALGORITHM, bcrypt_context, db_dependency,
    authenticate_user
)
from models import Users

router = APIRouter(
    prefix='/auth',
    tags=['🔐 auth']
)


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


templates = Jinja2Templates(directory="templates")


### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    """Login səhifəsini render edir."""
    return templates.TemplateResponse(request, "login.html")


@router.get("/register-page")
def render_register_page(request: Request):
    """Register səhifəsini render edir."""
    return templates.TemplateResponse(request, "register.html")


### Endpoints ###

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    """JWT token yaradır."""
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    """Yeni istifadəçi yaradır."""
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    """İstifadəçi girişi üçün JWT token qaytarır."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    # Cookie set et
    response.set_cookie(key="access_token", value=token, httponly=False, max_age=1800)

    return {'access_token': token, 'token_type': 'bearer'}
