
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional


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
    fecha_reporte: date
    id_ciudad: int
    nombre_ciudad: str
    nombre_provincia: str
    nombre_pais: str
    cantidad_clientes: int
    clientes: List[ReporteClientesPorCiudadDetalle]


class ReporteProductoDetalle(BaseModel):
    id_producto: int
    nombre_producto: str
    descripcion: str
    precio_compra: float
    precio_venta: float
    nombre_proveedor: str
    telefono_proveedor: str
    ciudad: str
    provincia:str
    pais:str

    class Config:
        from_attributes = True

class ReporteProveedorResponse(BaseModel):
    id_proveedor: int
    nombre_proveedor: str
    productos: List[ReporteProductoDetalle]
    
    
class ReporteStockDetalle(BaseModel):
    cantidad_en_sucursal: int
    cantidad_en_deposito: int
    
    nombre_sucursal: str
    nombre_deposito: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
    
class ReporteStockResumen(BaseModel):
    fecha_generacion: date 
    
    id_producto: int
    nombre_producto: str
    sku_producto: Optional[str] = None

    total_unidades_en_stock: int
    
    detalles_por_ubicacion: List[ReporteStockDetalle] 

    model_config = ConfigDict(from_attributes=True)
    
    
    