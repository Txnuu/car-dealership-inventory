"""Tests for authentication: registration, login, and the /me endpoint."""
from fastapi.testclient import TestClient


def test_register_user_success(client):
    """A new user can register with valid data."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secret123",
            "is_admin": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["is_admin"] is False
    # Password must never be returned.
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username_fails(client):
    """Registering the same username twice returns 409."""
    payload = {
        "username": "dup",
        "email": "dup@example.com",
        "password": "secret123",
    }
    client.post("/api/auth/register", json=payload)
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


def test_register_short_password_fails(client):
    """Passwords shorter than 6 characters are rejected (422)."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "short",
            "email": "short@example.com",
            "password": "123",
        },
    )
    assert response.status_code == 422


def test_register_invalid_email_fails(client):
    """Malformed emails are rejected by Pydantic validation."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "bademail",
            "email": "not-an-email",
            "password": "secret123",
        },
    )
    assert response.status_code == 422


def test_login_success(client):
    """A registered user can log in and receives a JWT."""
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "secret123",
        },
    )
    response = client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["is_admin"] is False


def test_login_wrong_password(client):
    """Logging in with the wrong password returns 401."""
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser2",
            "email": "loginuser2@example.com",
            "password": "secret123",
        },
    )
    response = client.post(
        "/api/auth/login",
        json={"username": "loginuser2", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Logging in with an unknown username returns 401."""
    response = client.post(
        "/api/auth/login",
        json={"username": "ghost", "password": "secret123"},
    )
    assert response.status_code == 401


def test_me_endpoint_returns_current_user(client):
    """The /me endpoint returns the authenticated user's profile."""
    client.post(
        "/api/auth/register",
        json={
            "username": "meuser",
            "email": "meuser@example.com",
            "password": "secret123",
        },
    )
    login = client.post(
        "/api/auth/login",
        json={"username": "meuser", "password": "secret123"},
    )
    token = login.json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"


def test_me_without_token_returns_401(client):
    """Calling /me without a token is rejected."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401 
