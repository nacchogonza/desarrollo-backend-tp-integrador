from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import date
from typing import List, Dict, Any, Optional
from .schemas import StockCreateRequest, StockResponse,ReporteStockDetalle, ReporteStockResumen
from api.core.models import (
    Stock,
    Producto,
    Proveedor,
    Ciudad,
    Provincia,
    Deposito,
    Sucursal,
)


async def obtener_stocks(db: AsyncSession):
    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(Stock.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(Stock.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()

async def crear_stock(db: AsyncSession, stock: StockCreateRequest):
    nuevo_stock = Stock(**stock.model_dump())
    db.add(nuevo_stock)
    await db.commit()
    await db.refresh(nuevo_stock)

    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(Stock.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(Stock.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Stock.id == nuevo_stock.id)
    )
    stock_con_relacion = result.scalar_one()
    return stock_con_relacion


async def delete_stock(db: AsyncSession, stock_id: int):
    stmt = select(Stock).where(Stock.id == stock_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False


""" async def reporte_stock_por_producto(db: AsyncSession, id_producto: int):
    # Traigo todos los stocks para ese producto
    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais),
            selectinload(Stock.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais),
            selectinload(Stock.producto)
            .selectinload(Producto.proveedor)   
            .selectinload(Proveedor.ciudad)     
            .selectinload(Ciudad.provincia)    
            .selectinload(Provincia.pais)  
        )
        .where(Stock.id_producto == id_producto)
    )
    return result.scalars().all() """

async def reporte_stock_por_producto(
    db: AsyncSession, 
    id_producto: int
) -> Dict[str, Any]: # Cambiamos el retorno a Dict[str, Any] para luego mapear a ReporteStockResumen
    
    # 1. Validar que el producto existe
    producto_result = await db.execute(
        select(Producto).where(Producto.id == id_producto)
    )
    producto_obj = producto_result.scalars().first()

    if not producto_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id_producto} no encontrado."
        )

    # 2. Traer todos los stocks para ese producto con todas las relaciones necesarias
    # Las opciones de selectinload las tienes bien definidas, las reutilizo.
    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.producto) # Ya que necesitas nombre/sku del producto en el resumen
            .selectinload(Producto.proveedor) 
            .selectinload(Proveedor.ciudad)   
            .selectinload(Ciudad.provincia)   
            .selectinload(Provincia.pais),   
            selectinload(Stock.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais),
            selectinload(Stock.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Stock.id_producto == id_producto)
        .order_by(Stock.id_sucursal.asc(), Stock.id_deposito.asc()) # Opcional: ordenar para mejor lectura
    )
    # Usar .unique() para evitar duplicados si los hay debido a los joins de selectinload
    items_stock = result.scalars().unique().all() 

    # 3. Procesar los datos para el resumen y los detalles
    total_unidades_en_stock = 0
    detalles_por_ubicacion: List[ReporteStockDetalle] = []

    for item in items_stock:
        # Sumamos las cantidades de sucursal y depósito para este registro de stock
        # y la sumamos al total general del reporte
        total_unidades_en_stock += item.cantidad_sucursal
        total_unidades_en_stock += item.cantidad_deposito

        detalles_por_ubicacion.append(
            ReporteStockDetalle(
                cantidad_en_sucursal=item.cantidad_sucursal,
                cantidad_en_deposito=item.cantidad_deposito,
                # Accedemos al nombre de la sucursal y depósito. Usamos "N/A" si es None.
                nombre_sucursal=item.sucursal.nombre if item.sucursal else "N/A",
                nombre_deposito=item.deposito.nombre if item.deposito else "N/A"
            )
        )

    # 4. Construir y retornar el diccionario que representa el ReporteStockResumen
    return {
        "fecha_generacion": date.today(),
        "id_producto": producto_obj.id,
        "nombre_producto": producto_obj.nombre,
        # Asumiendo que tu modelo Producto tiene un atributo 'sku'. Si no, será None.
        "sku_producto": producto_obj.sku if hasattr(producto_obj, 'sku') else None,
        "total_unidades_en_stock": total_unidades_en_stock,
        "detalles_por_ubicacion": detalles_por_ubicacion
    }



