"""Tests for inventory operations: purchase and restock."""
from fastapi.testclient import TestClient


def test_purchase_vehicle_success(client, admin_headers, user_headers):
    """A user can purchase a vehicle, reducing its quantity."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 2},
        headers=user_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3
    assert "purchased" in data["message"].lower()


def test_purchase_more_than_stock_fails(client, admin_headers, user_headers):
    """Purchasing more than available stock returns 400."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 2},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 5},
        headers=user_headers,
    )
    assert response.status_code == 400


def test_purchase_zero_quantity_fails(client, admin_headers, user_headers):
    """Purchasing zero units is rejected (422)."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 0},
        headers=user_headers,
    )
    assert response.status_code == 422


def test_purchase_out_of_stock_fails(client, admin_headers, user_headers):
    """Purchasing when quantity is already 0 returns 400."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 0},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/purchase",
        json={"quantity": 1},
        headers=user_headers,
    )
    assert response.status_code == 400


def test_purchase_without_auth_fails(client, admin_headers):
    """Unauthenticated purchase is rejected."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(f"/api/vehicles/{vehicle_id}/purchase", json={"quantity": 1})
    assert response.status_code == 401


def test_purchase_nonexistent_vehicle_returns_404(client, user_headers):
    """Purchasing a missing vehicle returns 404."""
    response = client.post(
        "/api/vehicles/9999/purchase",
        json={"quantity": 1},
        headers=user_headers,
    )
    assert response.status_code == 404


def test_restock_vehicle_as_admin(client, admin_headers):
    """Admin can restock a vehicle."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 3},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 7},
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 10
    assert "restocked" in data["message"].lower()


def test_restock_as_non_admin_forbidden(client, admin_headers, user_headers):
    """Regular users cannot restock."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 3},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 5},
        headers=user_headers,
    )
    assert response.status_code == 403


def test_restock_without_auth_fails(client, admin_headers):
    """Unauthenticated restock is rejected."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 3},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(f"/api/vehicles/{vehicle_id}/restock", json={"quantity": 5})
    assert response.status_code == 401


def test_restock_nonexistent_vehicle_returns_404(client, admin_headers):
    """Restocking a missing vehicle returns 404."""
    response = client.post(
        "/api/vehicles/9999/restock",
        json={"quantity": 5},
        headers=admin_headers,
    )
    assert response.status_code == 404


def test_restock_zero_quantity_fails(client, admin_headers):
    """Restocking zero units is rejected (422)."""
    create = client.post(
        "/api/vehicles",
        json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 3},
        headers=admin_headers,
    )
    vehicle_id = create.json()["id"]
    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 0},
        headers=admin_headers,
    )
    assert response.status_code == 422