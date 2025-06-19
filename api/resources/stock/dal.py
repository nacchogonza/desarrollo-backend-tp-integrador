from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    StockCreateRequest,
)
from api.core.models import Stock


async def obtener_stocks(db: AsyncSession):
    result = await db.execute(
        select(Stock).options(
            selectinload(Stock.producto)
            .selectinload(Stock.deposito)
            .selectinload(Stock.sucursal)
        )
    )
    return result.scalars().all()


async def crear_stock(db: AsyncSession, stock: StockCreateRequest):
    nuevo_stock = Stock(**stock.dict())
    db.add(nuevo_stock)
    await db.commit()
    await db.refresh(nuevo_stock)
    result = await db.execute(
        select(Stock)
        .options(
            selectinload(Stock.producto)
            .selectinload(Stock.deposito)
            .selectinload(Stock.sucursal)
        )
        .where(Stock.id == nuevo_stock.id)
    )
    stock_con_relacion = result.scalar_one()
    return stock_con_relacion
