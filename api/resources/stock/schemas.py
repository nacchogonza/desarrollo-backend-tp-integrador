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

# --- Nuevos Schemas para el Reporte de Stock por Producto ---

# Esquema para un detalle individual de stock en el reporte
# Representa la cantidad de un producto en una ubicación específica (sucursal/depósito)
class ReporteStockDetalle(BaseModel):
    cantidad_en_sucursal: int # Cantidad de este producto directamente en esta sucursal (para este registro de stock)
    cantidad_en_deposito: int # Cantidad de este producto en el depósito asociado a esta sucursal (para este registro de stock)
    
    nombre_sucursal: str
    nombre_deposito: Optional[str] = None # Será el nombre del depósito o "N/A" si no aplica

    model_config = ConfigDict(from_attributes=True)

# Esquema para el resumen completo del reporte de stock de UN producto
class ReporteStockResumen(BaseModel):
    fecha_generacion: date # Fecha en que se generó el reporte
    
    # Información del producto al que se refiere el reporte (en el resumen principal)
    id_producto: int
    nombre_producto: str
    sku_producto: Optional[str] = None # Asumiendo que el producto puede tener SKU

    total_unidades_en_stock: int # Suma total de todas las unidades de ESTE producto
    
    # La lista de dónde se encuentra el stock de este producto, detallado por ubicación
    detalles_por_ubicacion: List[ReporteStockDetalle] 

    model_config = ConfigDict(from_attributes=True)
