
from pydantic import BaseModel
from datetime import date
from typing import List


class ReporteVentasRequest(BaseModel):
    fecha_inicio: date
    fecha_fin: date


class ReporteVentaDetalle(BaseModel):
    id_remito: int
    fecha: date
    nombre_producto: str
    cantidad_vendida: int
    precio_unitario: float
    total_venta_item: float
    nombre_cliente: str
    nombre_sucursal: str

    class Config:
        from_attributes = True 

class ReporteVentasResponse(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    total_ventas_periodo: float
    cantidad_items_vendidos: int
    detalles_ventas: List[ReporteVentaDetalle] 
    
    
class ReporteClientesPorCiudadDetalle(BaseModel):
    id_cliente: int
    nombre: str
    telefono: str

    class Config:
        from_attributes = True 

class ReporteClientesPorCiudadResponse(BaseModel):
    id_ciudad: int
    nombre_ciudad: str
    nombre_provincia: str
    nombre_pais: str
    cantidad_clientes: int
    clientes: List[ReporteClientesPorCiudadDetalle]