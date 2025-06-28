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

    ciudad = relationship("Ciudad", back_populates="cliente")
    remito_devolucion = relationship(
        "RemitoDevolucion", back_populates="cliente", 
    )
    remito_venta = relationship(
        "RemitoVenta", back_populates="cliente", 
    )
    """ remito_venta = relationship(
        "RemitoVenta",
        back_populates="cliente",
        primaryjoin="Cliente.id == RemitoVenta.id_cliente",
        foreign_keys="[RemitoVenta.id_cliente]",
    ) """
    
    """ remito_venta = relationship(
        "RemitoVenta",
        back_populates="cliente",
        primaryjoin="Cliente.id == RemitoVenta.id_cliente",
        foreign_keys="[RemitoVenta.id_cliente]",
    ) """


class Ciudad(Base):
    __tablename__ = "ciudad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_provincia = Column(Integer, ForeignKey("provincia.id"))

    cliente = relationship("Cliente", back_populates="ciudad")
    provincia = relationship("Provincia", back_populates="ciudad")
    proveedor = relationship("Proveedor", back_populates="ciudad")
    sucursal = relationship("Sucursal", back_populates="ciudad")
    deposito = relationship("Deposito", back_populates="ciudad")


class Provincia(Base):
    __tablename__ = "provincia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"))

    ciudad = relationship("Ciudad", back_populates="provincia")
    pais = relationship("Pais", back_populates="provincia")


class Pais(Base):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)

    provincia = relationship("Provincia", back_populates="pais")


class RemitoCompra(Base):
    __tablename__ = "remito_compra"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_deposito = Column(Integer, ForeignKey("deposito.id"))

    proveedor = relationship("Proveedor", back_populates="remito_compra")
    producto = relationship("Producto", back_populates="remito_compra")
    deposito = relationship("Deposito", back_populates="remito_compra")


class RemitoVenta(Base):
    __tablename__ = "remito_venta"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))
    
    cliente = relationship("Cliente", back_populates="remito_venta")
    producto = relationship("Producto", back_populates="remito_venta")
    sucursal = relationship("Sucursal", back_populates="remito_venta")
    
    
    
    """ cliente = relationship(
        "Cliente",
        back_populates="remito_venta",
        primaryjoin="RemitoVenta.id_cliente == Cliente.id",
        foreign_keys="[RemitoVenta.id_cliente]",
    )
    
    producto = relationship(
        "Producto",
        back_populates="remito_venta",
        primaryjoin="RemitoVenta.id_producto == Producto.id",
        foreign_keys="[RemitoVenta.id_producto]",
    )
    
    sucursal = relationship(
        "Sucursal",
        back_populates="remito_venta",
        primaryjoin="RemitoVenta.id_sucursal == Sucursal.id",
        foreign_keys="[RemitoVenta.id_sucursal]",
    ) """


class RemitoDevolucion(Base):
    __tablename__ = "remito_devolucion"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, primary_key=False, nullable=False)
    cantidad = Column(Integer, primary_key=False, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))

    cliente = relationship("Cliente", back_populates="remito_devolucion")
    producto = relationship(
        "Producto", back_populates="remito_devolucion", 
    )
    sucursal = relationship(
        "Sucursal", back_populates="remito_devolucion"
    )


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

    deposito = relationship(
        "Deposito", back_populates="remito_transferencia"
    )
    producto = relationship(
        "Producto", back_populates="remito_transferencia"
    )
    sucursal = relationship(
        "Sucursal", back_populates="remito_transferencia"
    )


class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    precioCompra = Column(Float, nullable=False)
    precioVenta = Column(Float, nullable=False)

    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))

    remito_compra = relationship("RemitoCompra", back_populates="producto")
    remito_transferencia = relationship(
        "RemitoTransferencia", back_populates="producto"
    )
    remito_devolucion = relationship("RemitoDevolucion", back_populates="producto")

    proveedor = relationship("Proveedor", back_populates="producto")
    stock = relationship("Stock", back_populates="producto")
    remito_venta = relationship("RemitoVenta", back_populates="producto")

    """ stock = relationship(
        "Stock",
        back_populates="producto",
        primaryjoin="Producto.id == Stock.id_producto",
        foreign_keys="[Stock.id_producto]",
    )
    
    remito_venta = relationship(
        "RemitoVenta",
        back_populates="producto",
        primaryjoin="Producto.id == RemitoVenta.id_producto",
        foreign_keys="[RemitoVenta.id_producto]",
    ) """


class Proveedor(Base):
    __tablename__ = "proveedor"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)

    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))

    remito_compra = relationship("RemitoCompra", back_populates="proveedor")
    ciudad = relationship("Ciudad", back_populates="proveedor")
    producto = relationship("Producto", back_populates="proveedor")


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    cantidad_sucursal = Column(Integer, primary_key=False, index=False)
    cantidad_deposito = Column(Integer, primary_key=False, index=False)
    id_deposito = Column(Integer, ForeignKey("deposito.id"))
    id_sucursal = Column(
        Integer,
        ForeignKey("sucursal.id"),
    )
    id_producto = Column(
        Integer,
        ForeignKey("producto.id"),
    )

    deposito = relationship("Deposito", back_populates="stock")

    sucursal = relationship("Sucursal", back_populates="stock")
    producto = relationship("Producto", back_populates="stock")

    """ producto = relationship(
        "Producto",
        back_populates="stock",
        primaryjoin="Stock.id_producto == Producto.id",
        foreign_keys="[Stock.id_producto]",
    ) """


class Sucursal(Base):
    __tablename__ = "sucursal"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))

    ciudad = relationship("Ciudad", back_populates="sucursal")
    remito_devolucion = relationship(
        "RemitoDevolucion", back_populates="sucursal", 
    )
    remito_transferencia = relationship(
        "RemitoTransferencia", back_populates="sucursal", 
    )
    stock = relationship("Stock", back_populates="sucursal")
    remito_venta = relationship("RemitoVenta", back_populates="sucursal")
    
    """ remito_venta = relationship(
        "RemitoVenta",
        back_populates="sucursal",
        primaryjoin="Sucursal.id == RemitoVenta.id_sucursal",
        foreign_keys="[RemitoVenta.id_sucursal]",
    ) """


class Deposito(Base):
    __tablename__ = "deposito"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))

    ciudad = relationship("Ciudad", back_populates="deposito")
    remito_compra = relationship(
        "RemitoCompra", back_populates="deposito", 
    )
    remito_transferencia = relationship(
        "RemitoTransferencia", back_populates="deposito", 
    )
    stock = relationship("Stock", back_populates="deposito")
    
class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<DBUser(username='{self.username}', email='{self.email}')>"