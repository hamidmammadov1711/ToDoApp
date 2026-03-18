from fastapi.testclient import TestClient
import main
from fastapi import status

client = TestClient(main.app)

def test_healthy():
    response = client.get("/helathy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "API is healthy and running!"}


