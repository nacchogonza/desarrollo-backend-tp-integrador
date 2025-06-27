from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.resources.producto.schemas import (ProductoCreateRequest
)
from api.core.models import Producto, Proveedor, Ciudad, Provincia

async def obtener_productos(db: AsyncSession):
	result = await db.execute(select(Producto).options(
            selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        ))
	return result.scalars().all()

async def crear_producto(db: AsyncSession, producto: ProductoCreateRequest):
	nuevo_producto = Producto(**producto.dict())
	db.add(nuevo_producto)
	await db.commit()
	await db.refresh(nuevo_producto)
	result = await db.execute(
        select(Producto)
        .options(
            selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Producto.id == nuevo_producto.id)
    )


	producto = result.scalar_one()
    
	return producto

async def reporte_proveedores(db: AsyncSession, id_proveedor: int):
    result = await db.execute(
        select(Producto)
        .options(
            selectinload(Producto.proveedor) 
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        
        )
        .where(Producto.id_proveedor == id_proveedor)
    )
    Proveedores = result.scalars().all()
    return Proveedores