from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

# Define SQLAlchemy models
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    sale_date = Column(Date)
    quantity = Column(Integer)
    revenue = Column(Float)

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    stock_quantity = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models for request and response validation
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class SaleCreate(BaseModel):
    product_id: int
    sale_date: date
    quantity: int
    revenue: float

class InventoryUpdate(BaseModel):
    product_id: int
    stock_quantity: int

class SaleResponse(BaseModel):
    id: int
    product_id: int
    sale_date: date
    quantity: int
    revenue: float
    
class SaleQueryParams(BaseModel):
    start_date: date
    end_date: date
    category: str = None
    product_id: int = None
    
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    
    
class InventoryResponse(BaseModel):
    id: int
    product_id: int
    stock_quantity: int
    last_updated: str