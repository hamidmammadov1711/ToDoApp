from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from database import session_local  # database.py-dən gələn SessionLocal


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
