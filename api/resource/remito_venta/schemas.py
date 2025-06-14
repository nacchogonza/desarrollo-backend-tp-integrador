from datetime import date
from pydantic import BaseModel
#from ...resource.cliente.schemas import ClienteResponse
#from ...resource.producto.schemas import ProductoResponse
#from ...resource.sucursal.schemas import SucursalResponse


class RemitoVentaCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_cliente : int
    id_producto : int
    id_sucursal : int

class RemitoVentaResponse(BaseModel):
    fecha: date
    cantidad: int
    """cliente: ClienteResponse
    producto: ProductoResponse
    sucursal: SucursalResponse"""

    class Config:
        from_attributes = True