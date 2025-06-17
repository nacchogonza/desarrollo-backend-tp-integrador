from datetime import date
from pydantic import BaseModel
#from ...resources.cliente.schemas import ClienteResponse
#from ...resources.producto.schemas import ProductoResponse
#from ...resources.sucursal.schemas import ScursalResponse


class RemitoDevolucionCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_cliente : int
    id_producto : int
    id_sucursal : int

class RemitoDevolucionResponse(BaseModel):
    fecha: date
    cantidad: int
    cliente: ClienteResponse
    """producto: ProductoResponse
    sucursal: SucursalResponse"""

    class Config:
        from_attributes = True