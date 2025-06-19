from datetime import date
from pydantic import BaseModel
from ...resources.deposito.schemas import DepositoResponse
from ...resources.producto.schemas import ProductoResponse
from ...resources.sucursal.schemas import SucursalResponse

class RemitoTransferenciaCreateRequest(BaseModel):
    fecha : date
    cantidad : int
    id_deposito : int
    id_producto : int
    id_sucursal : int

class RemitoTransferenciaResponse(BaseModel):
    fecha: date
    cantidad: int
    deposito: DepositoResponse
    producto: ProductoResponse
    sucursal: SucursalResponse
    
    class Config:
       from_attributes = True