from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from datetime import date
from typing import List, Dict, Any

from ..core.models import RemitoVenta, Producto, Cliente, Sucursal 
from .schemas import ReporteVentaDetalle

async def get_ventas_by_period(
    db: AsyncSession,
    fecha_inicio: date,
    fecha_fin: date
) -> Dict[str, Any]:
    
    stmt = (
        select(RemitoVenta)
        .where(and_(
            RemitoVenta.fecha >= fecha_inicio,
            RemitoVenta.fecha <= fecha_fin
        ))
        .options(
            selectinload(RemitoVenta.producto),  
            selectinload(RemitoVenta.cliente),   
            selectinload(RemitoVenta.sucursal)   
        )
        .order_by(RemitoVenta.fecha.asc()) 
    )

    result = await db.execute(stmt)
    remitos_venta = result.scalars().unique().all()

    
    total_ventas_periodo = 0.0
    cantidad_items_vendidos = 0
    detalles_ventas: List[ReporteVentaDetalle] = []

    for remito in remitos_venta:
        
        total_venta_item = remito.cantidad * remito.producto.precioVenta
        total_ventas_periodo += total_venta_item
        cantidad_items_vendidos += remito.cantidad

        
        detalles_ventas.append(
            ReporteVentaDetalle(
                id_remito=remito.id,
                fecha=remito.fecha,
                nombre_producto=remito.producto.nombre,
                cantidad_vendida=remito.cantidad,
                precio_unitario=remito.producto.precioVenta,
                total_venta_item=total_venta_item,
                nombre_cliente=remito.cliente.nombre,
                nombre_sucursal=remito.sucursal.nombre
            )
        )

    
    return {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_ventas_periodo": total_ventas_periodo,
        "cantidad_items_vendidos": cantidad_items_vendidos,
        "detalles_ventas": detalles_ventas
    }
