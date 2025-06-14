from datetime import date
from pydantic import BaseModel
#from ...resource.deposito.schemas import DespositoResponse
#from ...resource.producto.schemas import ProductoResponse
#from ...resource.sucursal.schemas import SucursalResponse

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