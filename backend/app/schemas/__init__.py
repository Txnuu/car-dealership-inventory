"""Pydantic schemas for request validation and response serialization."""
from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_admin: bool = False


# ---------- Vehicles ----------
class VehicleCreate(BaseModel):
    make: str = Field(..., min_length=1, max_length=80)
    model: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class VehicleUpdate(BaseModel):
    make: str | None = Field(None, min_length=1, max_length=80)
    model: str | None = Field(None, min_length=1, max_length=80)
    category: str | None = Field(None, min_length=1, max_length=80)
    price: float | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class VehicleOut(BaseModel):
    id: int
    make: str
    model: str
    category: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


# ---------- Inventory ----------
class PurchaseRequest(BaseModel):
    quantity: int = Field(1, gt=0)


class RestockRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class InventoryActionResponse(BaseModel):
    id: int
    make: str
    model: str
    quantity: int
    message: str 
