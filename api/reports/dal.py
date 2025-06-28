from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import date
from typing import List, Dict, Any

from ..core.models import RemitoVenta, Cliente, Ciudad, Provincia, Pais, Producto, Proveedor
from .schemas import ReporteVentaDetalle, ReporteClientesPorCiudadDetalle, ReporteProductoDetalle, ReporteProveedorResponse
from datetime import date

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
    
    # Validamos primero que la ciudad existe. Si no existe devolvemos una excepcion y no ejecutamos el flujo del reporte
    ciudad = await db.execute(
        select(Ciudad)
        .where(Ciudad.id == id_ciudad)
        .options(
            selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    ciudad_obj = ciudad.scalars().first()

    if not ciudad_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La ciudad con ID {id_ciudad} no fue encontrada en la Base de Datos."
        )
    
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
    
    fecha_reporte = date.today()
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
        "fecha_reporte": fecha_reporte,
        "id_ciudad": id_ciudad,
        "nombre_ciudad": nombre_ciudad,
        "nombre_provincia": nombre_provincia,
        "nombre_pais": nombre_pais,
        "cantidad_clientes": cantidad_clientes,
        "clientes": clientes
    }

async def get_reporte_proveedor(db: AsyncSession, id_proveedor: int) -> Dict[str, Any]:
    stmt = (
        select(Producto)
        .where(Producto.id_proveedor == id_proveedor)
        .options(
            selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )

    result = await db.execute(stmt)
    productos = result.scalars().unique().all()

    if not productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"No se encontraron producto para el proveedor con ID {id_proveedor}"
        )
    
    proveedor = productos[0].proveedor #Todos los productos pertenecen al mismo proveedor

    productos_detalle = []
    for producto in productos:
        productos_detalle.append(
            ReporteProductoDetalle(
                id_producto=producto.id,
                nombre_producto=producto.nombre,
                descripcion=producto.descripcion,
                categoria=producto.categoria,
                precio_compra=producto.precioCompra,
                precio_venta=producto.precioVenta,
                nombre_proveedor=proveedor.nombre,
                telefono_proveedor=proveedor.telefono,
                ciudad=proveedor.ciudad.nombre,
                provincia=proveedor.ciudad.provincia.nombre,
                pais=proveedor.ciudad.provincia.pais.nombre
            )
        )

    return{
        "id_proveedor": proveedor.id,
        "nombre_proveedor": proveedor.nombre,
        "productos": productos_detalle
    }
