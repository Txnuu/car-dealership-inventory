"""Seed the database with 10 vehicles for demo purposes."""
from app.core.database import SessionLocal, engine, Base
from app.models import Vehicle

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

vehicles = [
    {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 25000, "quantity": 5, "image_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=400&h=250&fit=crop"},
    {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 22000, "quantity": 8, "image_url": "https://images.unsplash.com/photo-1606611013016-969c19ba27b8?w=400&h=250&fit=crop"},
    {"make": "Ford", "model": "Mustang", "category": "Coupe", "price": 35000, "quantity": 3, "image_url": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=400&h=250&fit=crop"},
    {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 30000, "quantity": 4, "image_url": "https://images.unsplash.com/photo-1568844293986-ca4c5c3b1c1c?w=400&h=250&fit=crop"},
    {"make": "BMW", "model": "X5", "category": "SUV", "price": 60000, "quantity": 2, "image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=250&fit=crop"},
    {"make": "Tesla", "model": "Model 3", "category": "Electric", "price": 45000, "quantity": 6, "image_url": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=400&h=250&fit=crop"},
    {"make": "Chevrolet", "model": "Silverado", "category": "Truck", "price": 38000, "quantity": 3, "image_url": "https://images.unsplash.com/photo-1583267746897-2cf415887172?w=400&h=250&fit=crop"},
    {"make": "Volkswagen", "model": "Golf", "category": "Hatchback", "price": 24000, "quantity": 7, "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=400&h=250&fit=crop"},
    {"make": "Mercedes", "model": "C-Class", "category": "Sedan", "price": 42000, "quantity": 3, "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400&h=250&fit=crop"},
    {"make": "Audi", "model": "Q5", "category": "SUV", "price": 48000, "quantity": 4, "image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=400&h=250&fit=crop"},
]

for v in vehicles:
    vehicle = Vehicle(**v)
    db.add(vehicle)

db.commit()
db.close()

print(f"✅ Successfully added {len(vehicles)} vehicles to the database!") 
