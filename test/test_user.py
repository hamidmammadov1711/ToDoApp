"""Test cases for user endpoints."""
from fastapi import status

from dependencies import get_db, get_current_user
from main import app
from .conftest import (
    override_get_db,
    override_get_current_user,
    client,
    test_user
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'hamidmammadovtest'
    assert response.json()['email'] == 'hamidmammadov@email.com'
    assert response.json()['first_name'] == 'Hamid'
    assert response.json()['last_name'] == 'Mammadov'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(994)-531-00-00'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={
        "password": "testpassword",
        "new_password": "newpassword"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={
        "password": "wrong_test_password",
        "new_password": "newpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == 204
