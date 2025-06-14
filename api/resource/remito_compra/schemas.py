from datetime import date
from pydantic import BaseModel
# RemitoCompraResponse tiene relaciones (proveedor, producto, deposito),
# importar sus Response Schemas aquí. Por ejemplo:
# from ...core.schemas import ProveedorResponse, ProductoResponse, DepositoResponse
# O si esas entidades también se mueven, la ruta cambiará. Por ahora, si no existen, déjalas comentadas.

class RemitoCompraCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_proveedor : int
    id_producto : int
    id_deposito : int

class RemitoCompraResponse(BaseModel):
    fecha: date
    cantidad: int
    """proveedor: ProveedorResponse
    producto: ProductoResponse
    deposito: DepositoResponse"""

    class Config:
        from_attributes = True
