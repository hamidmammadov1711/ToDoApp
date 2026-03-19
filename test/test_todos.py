"""Test cases for the todos API."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from dependencies import get_db, get_current_user
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


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"title": "Learn to code!",
         'complete': False, 'description': 'Need to learn everyday!',
         'id': 1,
         "priority": 5,
         'owner_id': 1
         }
    ]
