"""Shared test fixtures.

Each test module gets a fresh SQLite database file so tests are fully isolated.
We override the `get_db` dependency to point at the test database.
"""
import os
import tempfile

# Point the app at a temp SQLite file before importing anything that creates the engine.
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_db.name}"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.models import User
from app.core.security import hash_password

# Build a dedicated engine for the test database.
_test_engine = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

# Create all tables once for the test session.
Base.metadata.create_all(bind=_test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def reset_tables():
    """Clear all rows before each test so tests are fully isolated."""
    with _test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture(scope="function")
def client():
    """Return a TestClient."""
    return TestClient(app)


@pytest.fixture(scope="function")
def db():
    """Provide a test database session for direct DB assertions."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _register_and_login(client, username="testuser", password="password123", is_admin=False):
    """Helper: register a user and return the auth headers + token response."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": password,
            "is_admin": is_admin,
        },
    )
    assert response.status_code == 201, response.text
    login_resp = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, login_resp.json()


@pytest.fixture
def user_headers(client):
    headers, _ = _register_and_login(client)
    return headers


@pytest.fixture
def admin_headers(client):
    headers, _ = _register_and_login(client, username="admin", is_admin=True)
    return headers


@pytest.fixture
def sample_vehicle(client, admin_headers):
    """Create one vehicle via the API and return its JSON."""
    resp = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 5,
        },
        headers=admin_headers,
    )
    assert resp.status_code == 201, resp.text
    return resp.json() 
