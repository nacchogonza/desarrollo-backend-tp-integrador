from sqlalchemy import Column, Integer, String, ForeignKey, Date, VARCHAR, Float
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

class RemitoCompra(Base):
    __tablename__ = "Remito de Compra"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_deposito = Column(Integer, ForeignKey("deposito.id"))

    proveedor = relationship("Proveedor", back_populates="Remito de Compra", uselist=True)
    producto = relationship("Producto", back_populates="Remito de Compra", uselist=False)
    deposito = relationship("Deposito", back_populates="Remito de Compra", uselist=True)
    
class RemitoVenta(Base):
    __tablename__ = "Remito de Venta"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    cliente = relationship("Cliente", back_populates="Remito de Venta", uselist=True)
    producto = relationship("Producto", back_populates="Remito de Venta", uselist=False)
    sucursal = relationship("Sucursal", back_populates="Remito de Venta", uselist=True)

class RemitoDevolucion(Base):
    __tablename__ = "Remito de Devolución"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    cliente = relationship("Cliente", back_populates="Remito de Devolución", uselist=True)
    producto = relationship("Producto", back_populates="Remito de Devolución", uselist=False)
    sucursal = relationship("Sucursal", back_populates="Remito de Devolución", uselist=True)

class RemitoTransferencia(Base):
    __tablename__ = "Remito de Transferencia"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    origen = Column(VARCHAR, primary_key=False, nullable=False)
    destino = Column(VARCHAR, primary_key=False, nullable=False)
    id_deposito = Column(Integer, ForeignKey("deposito.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    deposito = relationship("Depósito", back_populates="Remito de Transferencia", uselist=True)
    producto = relationship("Producto", back_populates="Remito de Transferencia", uselist=True)
    sucursal = relationship("Sucursal", back_populates="Remito de Transferencia", uselist=True) 

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

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    cantidad_sucursal = Column(Integer, primary_key=False, index=False)
    cantidad_deposito = Column(Integer, primary_key=False, index=False)
    id_deposito = Column(Integer, ForeignKey("deposito.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    
    deposito = relationship("Deposito", back_populates="stock", uselist=False)
    sucursal = relationship("Sucursal", back_populates="stock", uselist=False)
    producto = relationship("Producto", back_populates="stock", uselist=False)
