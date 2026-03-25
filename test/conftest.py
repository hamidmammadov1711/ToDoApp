"""
Configuration and shared fixtures for the ToDoApp test suite.

Setup for testing environment.
Provides a Mock SQLite database and overrides FastAPI dependencies.
"""

import pytest
from sqlalchemy import StaticPool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from database import Base
from main import app
from models import Todos, Users
from dependencies import bcrypt_context

DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},
                       poolclass=StaticPool,
                       )

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override the database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    """Override the current user dependency for testing."""
    return {"username": "hamidmammadov", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    db = TestingSessionLocal()

    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )

    db.add(todo)
    db.commit()

    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="hamidmammadovtest",
        email="hamidmammadov@email.com",
        first_name="Hamid",
        last_name="Mammadov",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(994)-531-00-00"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
