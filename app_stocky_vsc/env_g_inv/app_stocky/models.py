from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, Integer, String, VARCHAR, Float, Date 
from sqlalchemy.orm import relationship
from .database import Base

class Proveedor(Base):
    __tablename__='proveedor'
    id=Column(Integer, primary_key=True, index=True)
    nombre=Column(String(250), nullable=False)
    telefono=Column(String(50), nullable=True)
    email=Column(String(50), nullable=True)
    direccion=Column(String(250), nullable=True)