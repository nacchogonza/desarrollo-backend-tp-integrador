from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    RemitoCompraCreateRequest,
)
from api.core.models import (
    RemitoCompra,
    Ciudad,
    Provincia,
    Producto,
    Proveedor,
    Deposito,
)


async def create_remito_compra(
    db: AsyncSession, remito_data: RemitoCompraCreateRequest
):

    db_remito = RemitoCompra(**remito_data.model_dump())
    db.add(db_remito)
    await db.commit()
    await db.refresh(db_remito)

    result = await db.execute(
        select(RemitoCompra)
        .options(
            selectinload(RemitoCompra.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoCompra.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoCompra.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .where(RemitoCompra.id == db_remito.id)
    )

    remito_compra_con_relacion = result.scalar_one()
    return remito_compra_con_relacion


async def get_remito_compra_by_id(db: AsyncSession, remito_id: int):

    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_remitos_compra(db: AsyncSession, skip: int = 0, limit: int = 100):

    stmt = (
        select(RemitoCompra)
        .options(
            selectinload(RemitoCompra.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoCompra.producto)
            .selectinload(Producto.proveedor)
            .selectinload(Proveedor.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .options(
            selectinload(RemitoCompra.deposito)
            .selectinload(Deposito.ciudad)
            .selectinload(Ciudad.provincia)
            .selectinload(Provincia.pais)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_remito_compra(
    db: AsyncSession, remito_id: int, remito_update: RemitoCompraCreateRequest
):

    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:

        for key, value in remito_update.model_dump(exclude_unset=True).items():
            setattr(db_remito, key, value)
        await db.commit()
        await db.refresh(db_remito)
        return db_remito
    return None


async def delete_remito_compra(db: AsyncSession, remito_id: int):

    stmt = select(RemitoCompra).where(RemitoCompra.id == remito_id)
    result = await db.execute(stmt)
    db_remito = result.scalar_one_or_none()

    if db_remito:
        await db.delete(db_remito)
        await db.commit()
        return True
    return False
