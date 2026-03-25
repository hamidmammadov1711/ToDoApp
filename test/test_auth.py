"""Test cases for auth endpoints."""
from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from dependencies import get_db, get_current_user, SECRET_KEY, ALGORITHM, authenticate_user
from main import app
from routers.auth import create_access_token
from .conftest import (
    override_get_db,
    TestingSessionLocal,
    test_user
)

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)

    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_exists_user = authenticate_user('WrongUserName', 'testpassword', db)
    assert non_exists_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY,
                               algorithms=[ALGORITHM],
                               options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


@pytest.mark.anyio
async def test_get_current_user_valid_token(test_user):
    encode = {
        'sub': test_user.username,
        'id': test_user.id,
        'role': test_user.role
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    # get_current_user returns a dict
    user = get_current_user(token=token)

    assert user is not None
    assert user['username'] == test_user.username
    assert user['id'] == test_user.id
    assert user['user_role'] == test_user.role


@pytest.mark.anyio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exceptionInfo:
        get_current_user(token=token)

    assert exceptionInfo.value.status_code == 401
    assert exceptionInfo.value.detail == 'Could not validate credentials'
