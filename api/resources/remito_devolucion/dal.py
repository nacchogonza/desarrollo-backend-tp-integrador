from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoDevolucionCreateRequest,
)
from api.core.models import (
    RemitoDevolucion,
    Cliente,
    Ciudad,
    Provincia,
    Producto,
    Proveedor,
    Sucursal,
)


async def create_remito_devolucion(
    db: AsyncSession, remito_data: RemitoDevolucionCreateRequest
):

    db_remito = RemitoDevolucion(**remito_data.model_dump())
    db.add(db_remito)
    await db.commit()
    await db.refresh(db_remito)

    result = await db.execute(
        select(RemitoDevolucion)
        .options(
            selectinload(RemitoDevolucion.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoDevolucion.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoDevolucion.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(RemitoDevolucion.id == db_remito.id)
    )

    remito_devolucion_con_relacion = result.scalar_one()
    return remito_devolucion_con_relacion


async def get_remito_devolucion_by_id(db: AsyncSession, remito_id: int):

    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # Obtiene un único resultado o None


async def get_all_remitos_devolucion(db: AsyncSession, skip: int = 0, limit: int = 100):

    stmt = (
        select(RemitoDevolucion)
        .options(
            selectinload(RemitoDevolucion.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoDevolucion.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoDevolucion.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_remito_devolucion(
    db: AsyncSession, remito_id: int, remito_update: RemitoDevolucionCreateRequest
):

    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:

        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None


async def delete_remito_devolucion(db: AsyncSession, remito_id: int):

    stmt = select(RemitoDevolucion).where(RemitoDevolucion.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False
