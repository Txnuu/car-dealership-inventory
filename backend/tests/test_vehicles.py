"""Tests for vehicle CRUD endpoints and authorization rules."""
from fastapi.testclient import TestClient


def test_add_vehicle_as_admin(client, admin_headers):
    """Admin can add a vehicle."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 10,
        },
        headers=admin_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["make"] == "Honda"
    assert data["model"] == "Civic"
    assert data["price"] == 22000
    assert data["quantity"] == 10
    assert "id" in data


def test_add_vehicle_as_non_admin_forbidden(client, user_headers):
    """Regular users cannot add vehicles (403)."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 10,
        },
        headers=user_headers,
    )
    assert response.status_code == 403


def test_add_vehicle_without_auth_forbidden(client):
    """Unauthenticated requests are rejected (401)."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 10,
        },
    )
    assert response.status_code == 401


def test_add_vehicle_invalid_price(client, admin_headers):
    """A non-positive price is rejected (422)."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": -100,
            "quantity": 10,
        },
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_add_vehicle_negative_quantity(client, admin_headers):
    """A negative quantity is rejected (422)."""
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": -5,
        },
        headers=admin_headers,
    )
    assert response.status_code == 422


def test_list_vehicles_requires_auth(client):
    """Listing vehicles is protected."""
    response = client.get("/api/vehicles")
    assert response.status_code == 401


def test_list_vehicles_returns_all(client, admin_headers, user_headers):
    """Authenticated users see all vehicles."""
    client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    client.post(
        "/api/vehicles",
        json={"make": "Ford", "model": "Mustang", "category": "Coupe", "price": 35000, "quantity": 3},
        headers=admin_headers,
    )
    response = client.get("/api/vehicles", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_vehicle_as_admin(client, admin_headers):
    """Admin can update vehicle fields."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={"price": 24000, "quantity": 8},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["price"] == 24000
    assert response.json()["quantity"] == 8
    # Untouched fields remain.
    assert response.json()["make"] == "Toyota"


def test_update_vehicle_non_admin_forbidden(client, admin_headers, user_headers):
    """Regular users cannot update vehicles."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={"price": 99999},
        headers=user_headers,
    )
    assert response.status_code == 403


def test_update_nonexistent_vehicle_returns_404(client, admin_headers):
    """Updating a missing vehicle returns 404."""
    response = client.put(
        "/api/vehicles/9999",
        json={"price": 10000},
        headers=admin_headers,
    )
    assert response.status_code == 404


def test_delete_vehicle_as_admin(client, admin_headers):
    """Admin can delete a vehicle."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=admin_headers)
    assert response.status_code == 204
    # Confirm it's gone.
    listing = client.get("/api/vehicles", headers=admin_headers)
    assert all(v["id"] != vehicle_id for v in listing.json())


def test_delete_vehicle_non_admin_forbidden(client, admin_headers, user_headers):
    """Regular users cannot delete vehicles."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=user_headers)
    assert response.status_code == 403


def test_delete_nonexistent_vehicle_returns_404(client, admin_headers):
    """Deleting a missing vehicle returns 404."""
    response = client.delete("/api/vehicles/9999", headers=admin_headers)
    assert response.status_code == 404