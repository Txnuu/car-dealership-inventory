"""Business logic for vehicles and inventory operations.

Keeping the logic here (rather than in the router) makes it easy to unit-test
and keeps the router layer thin.
"""
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Vehicle


def get_all_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).order_by(Vehicle.id).all()


def get_vehicle_or_404(db: Session, vehicle_id: int) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {vehicle_id} not found",
        )
    return vehicle


def create_vehicle(db: Session, data: dict) -> Vehicle:
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def update_vehicle(db: Session, vehicle: Vehicle, updates: dict) -> Vehicle:
    for field, value in updates.items():
        if value is not None:
            setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle: Vehicle) -> None:
    db.delete(vehicle)
    db.commit()


def search_vehicles(
    db: Session,
    make: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> list[Vehicle]:
    """Filter vehicles by any combination of make/model/category and price range."""
    query = db.query(Vehicle)
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if category:
        query = query.filter(Vehicle.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)
    return query.order_by(Vehicle.id).all()


def purchase_vehicle(db: Session, vehicle: Vehicle, quantity: int) -> Vehicle:
    """Reduce stock, raising 400 if there isn't enough inventory."""
    if vehicle.quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock: requested {quantity}, available {vehicle.quantity}",
        )
    vehicle.quantity -= quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle


def restock_vehicle(db: Session, vehicle: Vehicle, quantity: int) -> Vehicle:
    vehicle.quantity += quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle 
