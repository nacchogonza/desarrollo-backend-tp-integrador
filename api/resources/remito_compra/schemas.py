from datetime import date
from pydantic import BaseModel
from ...resources.proveedor.schemas import ProveedorResponse
from ...resources.producto.schemas import ProductoResponse
from ...resources.deposito.schemas import DepositoResponse

class RemitoCompraCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_proveedor : int
    id_producto : int
    id_deposito : int

class RemitoCompraResponse(BaseModel):
    fecha: date
    cantidad: int
    proveedor: ProveedorResponse
    producto: ProductoResponse
    deposito: DepositoResponse

    class Config:
        from_attributes = True
