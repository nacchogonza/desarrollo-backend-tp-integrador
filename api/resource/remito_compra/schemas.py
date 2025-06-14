from datetime import date
from pydantic import BaseModel
#from ...resource.proveedor.schemas import ProveedorResponse
#from ...resource.producto.schemas import ProductoResponse
#from ...resource.deposito.schemas import DepositoResponse

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
