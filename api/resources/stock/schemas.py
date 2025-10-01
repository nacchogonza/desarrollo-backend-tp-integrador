from pydantic import BaseModel, ConfigDict

from datetime import date
from typing import List, Optional

from ...resources.sucursal.schemas import SucursalResponse
from ...resources.deposito.schemas import DepositoResponse
from ...resources.producto.schemas import ProductoResponse

class StockCreateRequest(BaseModel):
    cantidad_sucursal: int
    cantidad_deposito: int
    id_producto: int
    id_sucursal: int
    id_deposito: int
    
class StockResponse(BaseModel):
    id: int
    cantidad_sucursal: int
    cantidad_deposito: int
    deposito: DepositoResponse
    sucursal: SucursalResponse
    producto: ProductoResponse

    model_config = ConfigDict(from_attributes=True)
