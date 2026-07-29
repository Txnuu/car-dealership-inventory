from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(80), nullable=False, index=True)
    model = Column(String(80), nullable=False, index=True)
    category = Column(String(80), nullable=False, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    image_url = Column(String(500), nullable=True)