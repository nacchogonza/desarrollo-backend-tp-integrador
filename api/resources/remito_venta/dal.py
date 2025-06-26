from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoVentaCreateRequest,
)
from api.core.models import (
    RemitoVenta,
    Cliente,
    Ciudad,
    Provincia,
    Producto,
    Proveedor,
    Sucursal,
)


async def create_remito_venta(db: AsyncSession, remito_data: RemitoVentaCreateRequest):
    nuevo_remito_venta = RemitoVenta(**remito_data.model_dump())
    db.add(nuevo_remito_venta)
    await db.commit()
    await db.refresh(nuevo_remito_venta)

    result = await db.execute(
        select(RemitoVenta)
        .options(
            selectinload(RemitoVenta.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoVenta.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoVenta.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(RemitoVenta.id == nuevo_remito_venta.id)
    )

    remito_venta_con_relacion = result.scalar_one()
    return remito_venta_con_relacion


async def get_remito_venta_by_id(db: AsyncSession, remito_id: int):

    stmt = select(RemitoVenta).where(RemitoVenta.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_remitos_venta(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = (
        select(RemitoVenta)
        .options(
            selectinload(RemitoVenta.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoVenta.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoVenta.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_remito_venta(
    db: AsyncSession, remito_id: int, remito_update: RemitoVentaCreateRequest
):

    stmt = select(RemitoVenta).where(RemitoVenta.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:

        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None


async def delete_remito_venta(db: AsyncSession, remito_id: int):

    stmt = select(RemitoVenta).where(RemitoVenta.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False
