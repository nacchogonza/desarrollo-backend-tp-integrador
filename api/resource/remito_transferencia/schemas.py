from datetime import date
from pydantic import BaseModel
# Si RemitoCompraResponse tiene relaciones (proveedor, producto, deposito),
# necesitarás importar sus Response Schemas aquí. Por ejemplo:
# from ...core.schemas import ProveedorResponse, ProductoResponse, DepositoResponse
# O si esas entidades también se mueven, la ruta cambiará. Por ahora, si no existen, déjalas comentadas.

class RemitoTransferenciaCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_deposito : int
    id_producto : int
    id_sucursal : int

class RemitoTransferenciaResponse(BaseModel):
    fecha: date
    cantidad: int
    """deposito: DepositoResponse
    producto: ProductoResponse
    sucursal: SucursalResponse"""
    
    class Config:
       from_attributes = True