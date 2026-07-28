from fastapi import FastAPI
from app.core.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Dealership Inventory API")

@app.get("/")
def root():
    return {"message": "Car Dealership API is running"} 
