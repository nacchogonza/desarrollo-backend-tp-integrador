from datetime import date
from pydantic import BaseModel
from datetime import date

from api.resources.location.schemas import CiudadResponse
from api.resources.cliente.schemas import ClienteResponse


# REQUEST
class SucursalCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int


class DepositoCreateRequest(BaseModel):
    nombre: str
    telefono: int
    email: str
    direccion: str
    id_ciudad: int


class RemitoCompraCreateRequest(BaseModel):
    fecha: date
    cantidad: int
    """ id_proveedor: int
    id_producto: int
    id_deposito: int """


class RemitoVentaCreateRequest(BaseModel):
    fecha: date
    cantidad: int
    """ id_cliente: int
    id_producto: int
    id_sucursal: int """


class RemitoDevolucionCreateRequest(BaseModel):
    fecha: date
    cantidad: int
    """ id_cliente: int
    id_producto: int
    id_sucursal: int """


class RemitoTransferenciaCreateRequest(BaseModel):
    fecha: date
    cantidad: int
    """ id_deposito: int
    id_producto: int
    id_sucursal: int """


class ProductoCreateRequest(BaseModel):
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    id_proveedor: int
    id_stock: int

class ProveedorCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int


# RESPONSE
class RemitoCompraResponse(BaseModel):
    fecha: date
    cantidad: int
    """proveedor: ProveedorResponse
    producto: ProductoResponse
    deposito: DepositoResponse"""

    class Config:
        orm_mode = True


class RemitoVentaRequest(BaseModel):
    fecha: date
    cantidad: int
    cliente: ClienteResponse
    """producto: ProductoResponse
    sucursal: SucursalResponse"""

    class Config:
        orm_mode = True


class RemitoDevolucionRequest(BaseModel):
    fecha: date
    cantidad: int
    cliente: ClienteResponse
    """producto: ProductoResponse
    sucursal: SucursalResponse"""


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    categoria: str
    precioCompra: float
    precioVenta: float

    class Config:
        orm_mode = True


class RemitoTransferenciaRequest(BaseModel):
    fecha: date
    cantidad: int
    """deposito: DepositoResponse
    producto: ProductoResponse
    sucursal: SucursalResponse"""


class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str

    class Config:
        orm_mode = True

class SucursalResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True
        
class DepositoResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str

    class Config:
        orm_mode = True
