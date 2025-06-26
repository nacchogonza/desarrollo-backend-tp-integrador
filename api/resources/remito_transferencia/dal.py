from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoTransferenciaCreateRequest,
)
from api.core.models import (
    RemitoTransferencia,
    Cliente,
    Ciudad,
    Provincia,
    Producto,
    Proveedor,
    Sucursal,
)


async def create_remito_transferencia(
    db: AsyncSession, remito_data: RemitoTransferenciaCreateRequest
):

    db_remito = RemitoTransferencia(**remito_data.model_dump())
    db.add(db_remito)
    await db.commit()
    await db.refresh(db_remito)

    result = await db.execute(
        select(RemitoTransferencia)
        .options(
            selectinload(RemitoTransferencia.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoTransferencia.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoTransferencia.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(RemitoTransferencia.id == db_remito.id)
    )

    remito_transferencia_con_relacion = result.scalar_one()
    return remito_transferencia_con_relacion


async def get_remito_transferencia_by_id(db: AsyncSession, remito_id: int):

    stmt = select(RemitoTransferencia).where(RemitoTransferencia.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_remitos_transferencia(
    db: AsyncSession, skip: int = 0, limit: int = 100
):

    stmt = (
        select(RemitoTransferencia)
        .options(
            selectinload(RemitoTransferencia.cliente)
            .selectinload(Cliente.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoTransferencia.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoTransferencia.sucursal)
            .selectinload(Sucursal.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_remito_transferencia(
    db: AsyncSession, remito_id: int, remito_update: RemitoTransferenciaCreateRequest
):

    stmt = select(RemitoTransferencia).where(RemitoTransferencia.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:

        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None


async def delete_remito_transferencia(db: AsyncSession, remito_id: int):

    stmt = select(RemitoTransferencia).where(RemitoTransferencia.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False
