from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

from dependencies import db_dependency, authenticate_user, bcrypt_context
from models import Users

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


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    """
        This function is a placeholder for a route handler that would handle user login and token generation.
        In a real application, you would implement logic to authenticate the user, verify their credentials, and generate a JWT or similar token for access control.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return {'Failed Authentication': 'Invalid username or password'}

    return {'Successful Authentication'}
