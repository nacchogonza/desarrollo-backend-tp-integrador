from datetime import date
from pydantic import BaseModel
from datetime import date


# REQUEST
class ClienteCreateRequest(BaseModel):
    nombre: str
    telefono: str
    email: str
    direccion: str
    id_ciudad: int


class PaisCreateRequest(BaseModel):
    nombre: str


class ProvinciaCreateRequest(BaseModel):
    nombre: str
    id_pais: int


class CiudadCreateRequest(BaseModel):
    nombre: str
    id_provincia: int


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


class ProveedorCreateRequest(BaseModel):
    nombre: str
    direccion: str
    id_ciudad: int
    telefono: str
    email: str
    condicionRecepcion: date


class StockCreateRequest(BaseModel):
    cantidad_sucursal: int
    cantidad_deposito: int
    id_producto: int
    id_sucursal: int
    id_deposito: int


# RESPONSE
class PaisResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class ProvinciaResponse(BaseModel):
    id: int
    nombre: str
    pais: PaisResponse

    class Config:
        orm_mode = True


class CiudadResponse(BaseModel):
    id: int
    nombre: str
    provincia: ProvinciaResponse

    class Config:
        orm_mode = True


class ClienteResponse(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    direccion: str
    ciudad: CiudadResponse

    class Config:
        orm_mode = True


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
    nombre: str
    direccion: str
    telefono: str
    email: str
    condicionRecepcion: date
    ciudad: CiudadResponse

    class Config:
        orm_mode = True


class StockResponse(BaseModel):
    id: int
    cantidad_sucursal: int
    cantidad_deposito: int
    """ deposito: DepositoResponse
    sucursal: SucursalResponse
    producto: ProductoResponse """

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
