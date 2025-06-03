from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from api.core.database import Base


class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))
    
    ciudad = relationship("Ciudad", back_populates="cliente", uselist=False)
    
class Ciudad(Base):
    __tablename__ = "ciudad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_provincia = Column(Integer, ForeignKey("provincia.id"))
    
    cliente = relationship("Cliente", back_populates="ciudad", uselist=False)
    provincia = relationship("Provincia", back_populates="ciudad", uselist=False)
    proveedor = relationship("Proveedor", back_populates="ciudad", uselist=False)
    
class Provincia(Base):
    __tablename__ = "provincia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"))
    
    ciudad = relationship("Ciudad", back_populates="provincia", uselist=False)
    pais = relationship("Pais", back_populates="provincia", uselist=False)
    
class Pais(Base):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)

    provincia = relationship("Provincia", back_populates="pais", uselist=False)

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)  
    nombre = Column(String, primary_key=False, nullable=False)
    descripcion = Column(String, primary_key=False, nullable=False)
    categoria = Column(String, primary_key=False, nullable=False)
    precioCompra = Column(Float, primary_key=False, nullable=False)
    precioVenta = Column(Float, primary_key=False, nullable=False)

    detalleOrdenVenta = relationship("DetalleOrdenVenta", back_populates="producto", uselist=False)
    detalleOrdenCompra = relationship("DetalleOrdenCompra", back_populates="producto", uselist=False)
    stock = relationship("Stock",back_populates="producto", uselist=False)

class Proveedor(Base):
    __tablename__ = "proveedor"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable= False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer,ForeignKey("ciudad.id"))    
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    condicionRecepcion = Column(Date, primary_key=False, nullable=False)

    remitoCompra = relationship("RemitoCompra", back_populates="proveedor", uselist=False)
    ciudad = relationship("Ciudad", back_populates="proveedor", uselist=False)