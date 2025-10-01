from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import StockCreateRequest
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
