from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import session_local  # database.py-dən gələn SessionLocal
from models import Users

# Initialize bcrypt context for password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    """
        This function is a dependencies function that provides a database session for use in FastAPI routes.
        It creates a new database session using the session_local function, yields it for use in the route, and ensures that the session is properly closed after the route is finished executing.
        This allows for efficient management of database connections and resources in a FastAPI application.

    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    """
        This function is a placeholder for a user authentication function. In a real application, you would implement logic to verify the provided username and password against stored user credentials in the database.
        The function would typically return a user object if the authentication is successful or None if it fails.

    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    # Here you would add logic to verify the password, e.g., using bcrypt to compare the hashed password
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True
