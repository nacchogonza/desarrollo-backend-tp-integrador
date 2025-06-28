from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from datetime import date
from typing import List, Dict, Any

from ..core.models import RemitoVenta, Cliente, Ciudad, Provincia
from .schemas import ReporteVentaDetalle, ReporteClientesPorCiudadDetalle

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
    
async def get_clientes_by_city(
    db: AsyncSession,
    id_ciudad: int
) -> Dict[str, Any]:
    
    result = await db.execute(
        select(Cliente)
        .where(Cliente.id_ciudad == id_ciudad)
        .options(
            selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    
    clientes_por_ciudad = result.scalars().unique().all()
    
    cantidad_clientes = 0
    nombre_ciudad = ""
    nombre_provincia = ""
    nombre_pais = ""
    clientes: List[ReporteClientesPorCiudadDetalle] = []

    for cliente in clientes_por_ciudad:
        
        cantidad_clientes += 1
        if (nombre_ciudad == "" and nombre_provincia == "" and nombre_pais == ""):
            nombre_ciudad = cliente.ciudad.nombre
            nombre_provincia = cliente.ciudad.provincia.nombre
            nombre_pais = cliente.ciudad.provincia.pais.nombre
        
        clientes.append(
            ReporteClientesPorCiudadDetalle(
                id_cliente = cliente.id,
                nombre = cliente.nombre,
                telefono = cliente.telefono
            )
        )

    
    return {
        "id_ciudad": id_ciudad,
        "nombre_ciudad": nombre_ciudad,
        "nombre_provincia": nombre_provincia,
        "nombre_pais": nombre_pais,
        "cantidad_clientes": cantidad_clientes,
        "clientes": clientes
    }