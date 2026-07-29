"""Tests for the /api/vehicles/search endpoint."""
from fastapi.testclient import TestClient


def _seed(client, admin_headers):
    """Seed a small inventory for search tests."""
    vehicles = [
        {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 30000, "quantity": 3},
        {"make": "Ford", "model": "Mustang", "category": "Coupe", "price": 35000, "quantity": 2},
        {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 22000, "quantity": 8},
        {"make": "BMW", "model": "X5", "category": "SUV", "price": 60000, "quantity": 1},
    ]
    for v in vehicles:
        client.post("/api/vehicles", json=v, headers=admin_headers)


def test_search_requires_auth(client):
    """Search is protected."""
    response = client.get("/api/vehicles/search")
    assert response.status_code == 401


def test_search_no_filters_returns_all(client, admin_headers, user_headers):
    """With no filters, all vehicles are returned."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_search_by_make(client, admin_headers, user_headers):
    """Filtering by make returns matching vehicles (case-insensitive)."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?make=toyota", headers=user_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert all(r["make"] == "Toyota" for r in results)


def test_search_by_category(client, admin_headers, user_headers):
    """Filtering by category returns matching vehicles."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?category=SUV", headers=user_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert all(r["category"] == "SUV" for r in results)


def test_search_by_model(client, admin_headers, user_headers):
    """Filtering by model returns matching vehicles."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?model=civic", headers=user_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["model"] == "Civic"


def test_search_by_price_range(client, admin_headers, user_headers):
    """Filtering by min and max price returns vehicles in range."""
    _seed(client, admin_headers)
    response = client.get(
        "/api/vehicles/search?min_price=22000&max_price=30000",
        headers=user_headers,
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 3
    for r in results:
        assert 22000 <= r["price"] <= 30000


def test_search_by_min_price_only(client, admin_headers, user_headers):
    """Only min_price is applied."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?min_price=35000", headers=user_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for r in results:
        assert r["price"] >= 35000


def test_search_by_max_price_only(client, admin_headers, user_headers):
    """Only max_price is applied."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?max_price=25000", headers=user_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    for r in results:
        assert r["price"] <= 25000


def test_search_combined_filters(client, admin_headers, user_headers):
    """Multiple filters combine with AND logic."""
    _seed(client, admin_headers)
    response = client.get(
        "/api/vehicles/search?make=Toyota&category=SUV",
        headers=user_headers,
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["model"] == "RAV4"


def test_search_no_matches(client, admin_headers, user_headers):
    """A filter that matches nothing returns an empty list."""
    _seed(client, admin_headers)
    response = client.get("/api/vehicles/search?make=Lamborghini", headers=user_headers)
    assert response.status_code == 200
    assert response.json() == []