from sqlalchemy import Column, Integer, String, ForeignKey, Date, VARCHAR, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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
    remito_venta = relationship("RemitoVenta", back_populates="cliente", uselist=False)
    remito_devolucion = relationship("RemitoDevolucion", back_populates="cliente", uselist=False)
    
class Ciudad(Base):
    __tablename__ = "ciudad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_provincia = Column(Integer, ForeignKey("provincia.id"))
    
    cliente = relationship("Cliente", back_populates="ciudad", uselist=False)
    provincia = relationship("Provincia", back_populates="ciudad", uselist=False)
    proveedor = relationship("Proveedor", back_populates="ciudad", uselist=False)
    sucursal = relationship("Sucursal", back_populates="ciudad", uselist=False)
    deposito = relationship("Deposito", back_populates="ciudad", uselist=False)
    
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
    __tablename__ = "remito_compra"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_deposito = Column(Integer, ForeignKey("deposito.id"))

    proveedor = relationship("Proveedor", back_populates="remito_compra", uselist=True)
    producto = relationship("Producto", back_populates="remito_compra", uselist=False)
    deposito = relationship("Deposito", back_populates="remito_compra", uselist=True)
    
class RemitoVenta(Base):
    __tablename__ = "remito_venta"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    cliente = relationship("Cliente", back_populates="remito_venta", uselist=True)
    producto = relationship("Producto", back_populates="remito_venta", uselist=False)
    sucursal = relationship("Sucursal", back_populates="remito_venta", uselist=True)

class RemitoDevolucion(Base):
    __tablename__ = "remito_devolucion"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    cliente = relationship("Cliente", back_populates="remito_devolucion", uselist=True)
    producto = relationship("Producto", back_populates="remito_devolucion", uselist=False)
    sucursal = relationship("Sucursal", back_populates="remito_devolucion", uselist=True)

class RemitoTransferencia(Base):
    __tablename__ = "remito_transferencia"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    origen = Column(VARCHAR, primary_key=False, nullable=False)
    destino = Column(VARCHAR, primary_key=False, nullable=False)
    id_deposito = Column(Integer, ForeignKey("deposito.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    deposito = relationship("Deposito", back_populates="remito_transferencia", uselist=True)
    producto = relationship("Producto", back_populates="remito_transferencia", uselist=True)
    sucursal = relationship("Sucursal", back_populates="remito_transferencia", uselist=True) 

class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    precioCompra = Column(Float, nullable=False)
    precioVenta = Column(Float, nullable=False)

    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    # id_stock = Column(Integer, ForeignKey("stock.id")) # <--- ¡Esta FK en Producto causa el problema!

    remito_compra = relationship("RemitoCompra", back_populates="producto")
    remito_venta = relationship("RemitoVenta", back_populates="producto")
    remito_transferencia = relationship("RemitoTransferencia", back_populates="producto")
    remito_devolucion = relationship("RemitoDevolucion", back_populates="producto")

    proveedor = relationship("Proveedor", back_populates="producto", uselist=False)

    # Corregido: La relación 'stock' en Producto usará la FK 'id_producto' en el modelo Stock
    stock = relationship(
        "Stock",
        back_populates="producto",
        uselist=False,
        primaryjoin="Producto.id == Stock.id_producto", # <--- Especifica la condición de unión
        foreign_keys="[Stock.id_producto]" # <--- Especifica la clave foránea en la tabla Stock
    )
   

class Proveedor(Base):
    __tablename__ = "proveedor"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable= False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)

    id_ciudad = Column(Integer,ForeignKey("ciudad.id"))    

    remito_compra = relationship("RemitoCompra", back_populates="proveedor")
    ciudad = relationship("Ciudad", back_populates="proveedor", uselist=False)
    producto = relationship("Producto", back_populates="proveedor")

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    cantidad_sucursal = Column(Integer, primary_key=False, index=False)
    cantidad_deposito = Column(Integer, primary_key=False, index=False)
    id_deposito = Column(Integer, ForeignKey("deposito.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"), unique=True) # <--- Añadir unique=True si es 1-1

    deposito = relationship("Deposito", back_populates="stock", uselist=False)
    sucursal = relationship("Sucursal", back_populates="stock", uselist=False)

    # Corregido: La relación 'producto' en Stock usará la FK 'id_producto' en sí misma
    producto = relationship(
        "Producto",
        back_populates="stock",
        uselist=False,
        primaryjoin="Stock.id_producto == Producto.id", # <--- Especifica la condición de unión
        foreign_keys="[Stock.id_producto]" # <--- Especifica la clave foránea en la tabla Stock
    )

class Sucursal(Base):
    __tablename__= "sucursal"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))

    ciudad = relationship("Ciudad", back_populates="sucursal", uselist=False)
    remito_venta = relationship("RemitoVenta", back_populates="sucursal", uselist=False)
    remito_devolucion = relationship("RemitoDevolucion", back_populates="sucursal", uselist=False)
    remito_transferencia = relationship("RemitoTransferencia", back_populates="sucursal", uselist=False)
    stock = relationship("Stock", back_populates="sucursal", uselist=False)

class Deposito(Base):
    __tablename__= "deposito"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(Integer, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))

    ciudad = relationship("Ciudad", back_populates="deposito", uselist=False)
    remito_compra = relationship("RemitoCompra", back_populates="deposito", uselist=False)
    remito_transferencia = relationship("RemitoTransferencia", back_populates="deposito", uselist=False)
    stock = relationship("Stock", back_populates="deposito", uselist=False)

class DBUser(Base):
    __tablename__ = "users" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String) # Aquí se guardará la contraseña hasheada
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now()) # Fecha de creación
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) # Fecha de última actualización

    # Puedes añadir un método __repr__ para una representación más legible en el debugger
    def __repr__(self):
        return f"<DBUser(username='{self.username}', email='{self.email}')>"