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
from models import Todos

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

    class MockUser:
        id = 1
        username = "hamidmammadov"
        role = "admin"

    return MockUser()


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
