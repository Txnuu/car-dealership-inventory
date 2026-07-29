"""FastAPI application entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, vehicles

# Create tables on startup. In a real app you'd use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Dealership Inventory System",
    description="REST API for managing a car dealership's vehicle inventory.",
    version="1.0.0",
)

# Allow the Vite dev server (and any deployed frontend) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://car-dealership-inventory-one.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vehicles.router)


@app.get("/", tags=["health"])
def root() -> dict:
    return {"status": "ok", "service": "Car Dealership Inventory API"}