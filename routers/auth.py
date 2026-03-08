from fastapi import APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from dependencies import db_dependency
from models import Users

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
