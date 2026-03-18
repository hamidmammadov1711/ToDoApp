"""Test cases for the FastAPI application defined in main.py."""
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthy():
    response = client.get("/helathy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API is healthy and running!"}
