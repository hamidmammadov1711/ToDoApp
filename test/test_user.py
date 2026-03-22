from fastapi import status

from dependencies import get_db, get_current_user
from main import app
from models import Todos
from dependencies import verify_password,hash_password
from .conftest import (
    override_get_db,
    override_get_current_user,
    TestingSessionLocal,
    client,
    test_user
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ['username'] == 'hamidmammadovtest'
    assert response.json() ['email'] == 'hamidmammadov@email.com'
    assert response.json() ['first_name'] == 'Hamid'
    assert response.json() ['last_name'] == 'Mammadov'
    assert response.json() ['role'] == 'admin'
    assert response.json() ['phone_number'] == '(994)-531-00-00'