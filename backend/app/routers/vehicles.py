"""Vehicle and inventory routes."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models import User, Vehicle
from app.services import inventory_service
from app.schemas import (
    InventoryActionResponse,
    PurchaseRequest,
    RestockRequest,
    VehicleCreate,
    VehicleOut,
    VehicleUpdate,
)

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleOut])
def list_vehicles(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Vehicle]:
    """Return every vehicle in the inventory (authenticated)."""
    return inventory_service.get_all_vehicles(db)


@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def add_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Vehicle:
    """Add a new vehicle (admin only)."""
    return inventory_service.create_vehicle(db, payload.model_dump())


@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(
    make: str | None = Query(None),
    model: str | None = Query(None),
    category: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Vehicle]:
    """Search vehicles by make, model, category, or price range (authenticated)."""
    return inventory_service.search_vehicles(
        db, make=make, model=model, category=category, min_price=min_price, max_price=max_price
    )

@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Vehicle:
    """Get a single vehicle by ID (authenticated)."""
    return inventory_service.get_vehicle_or_404(db, vehicle_id)


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Vehicle:
    """Update a vehicle's details (admin only)."""
    vehicle = inventory_service.get_vehicle_or_404(db, vehicle_id)
    return inventory_service.update_vehicle(db, vehicle, payload.model_dump(exclude_unset=True))


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> None:
    """Delete a vehicle (admin only)."""
    vehicle = inventory_service.get_vehicle_or_404(db, vehicle_id)
    inventory_service.delete_vehicle(db, vehicle)


@router.post("/{vehicle_id}/purchase", response_model=InventoryActionResponse)
def purchase_vehicle(
    vehicle_id: int,
    payload: PurchaseRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict:
    """Purchase a vehicle, reducing its stock."""
    vehicle = inventory_service.get_vehicle_or_404(db, vehicle_id)
    inventory_service.purchase_vehicle(db, vehicle, payload.quantity)
    return {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "quantity": vehicle.quantity,
        "message": f"Successfully purchased {payload.quantity} unit(s)",
    }


@router.post("/{vehicle_id}/restock", response_model=InventoryActionResponse)
def restock_vehicle(
    vehicle_id: int,
    payload: RestockRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict:
    """Restock a vehicle (admin only)."""
    vehicle = inventory_service.get_vehicle_or_404(db, vehicle_id)
    inventory_service.restock_vehicle(db, vehicle, payload.quantity)
    return {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "quantity": vehicle.quantity,
        "message": f"Successfully restocked {payload.quantity} unit(s)",
    } 
