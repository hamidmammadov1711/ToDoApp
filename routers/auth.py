from datetime import timedelta, datetime, timezone
from typing import Annotated
import os
from dotenv import load_dotenv

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from starlette import status
from dependencies import db_dependency, authenticate_user, bcrypt_context
from models import Users

# Load environment variables from .env file
load_dotenv()

# Retrieve SECRET_KEY and ALGORITHM from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()

class CreateUserRequest(BaseModel):
    """
    This class defines a Pydantic model for a user request. It includes fields for username, email, first name, last name, and password.
    """
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str  # New field to specify the user's role (e.g., "admin", "user", etc.)


class TokenResponse(BaseModel):
    """
    This class defines a Pydantic model for a token response. It includes fields for the access token and the token type.
    """
    access_token: str
    token_type: str


@router.post("/auth", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency,
                create_user_request: CreateUserRequest):
    """
        This function is a route handler for a POST request to the "/auth" endpoint.
    """
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        # In a real application, you should hash the password before storing it
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
        This function is a placeholder for a route handler that would handle user login and token generation.
        In a real application, you would implement logic to authenticate the user, verify their credentials, and generate a JWT or similar token for access control.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return {'Failed Authentication': 'Invalid username or password'}

    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


def create_access_token(usename: str, user_id: int, expires_delta: timedelta):
    """
        This function is a placeholder for a function that would create an access token (e.g., JWT) for authenticated users.
        In a real application, you would implement logic to generate a token that includes user information and an expiration time, and then return this token to the client for use in subsequent authenticated requests.
    """
    encode = {"sub": usename, "user_id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    # Here you would use a library like PyJWT to encode the token with the SECRET_KEY
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
