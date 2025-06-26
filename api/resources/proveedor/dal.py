from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.resources.proveedor.schemas import ProveedorCreateRequest
from api.core.models import Proveedor, Ciudad, Provincia, Producto


async def obtener_proveedor(db: AsyncSession):
    result = await db.execute(
        select(Proveedor).options(
            selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    return result.scalars().all()


""" result = await db.execute(select(Producto).options(
            selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        ))
	return result.scalars().all() """


async def crear_proveedor(db: AsyncSession, proveedor: ProveedorCreateRequest):
    nuevo_proveedor = Proveedor(**proveedor.dict())
    db.add(nuevo_proveedor)
    await db.commit()
    await db.refresh(nuevo_proveedor)
    
    result = await db.execute(
        select(Proveedor)
        .options(
            selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(Proveedor.id == nuevo_proveedor.id)
    )
    proveedor_con_relacion = result.scalar_one()
    return proveedor_con_relacion

#FUNCIONALIDAD REPORTE DE PROVEEDORES

async def reporte_proveedores(db: AsyncSession):
    result = await db.execute(
        select(Proveedor)
        .options(
            selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais),
            selectinload(Proveedor.producto)
        )
    )
    Proveedores = result.scalars().all()
    return Proveedores