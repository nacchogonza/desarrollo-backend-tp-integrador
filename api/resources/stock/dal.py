from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .schemas import (
    StockCreateRequest,
    StockResponse
)
from api.core.models import Stock, Producto


async def obtener_stocks(db: AsyncSession):
    result = await db.execute(
        select(Stock)
        .options(selectinload(Stock.producto))
        .options(selectinload(Stock.deposito))
        .options(selectinload(Stock.sucursal))
    )
    return result.scalars().all()


""" async def crear_stock(db: AsyncSession, stock: StockCreateRequest):
    nuevo_stock = Stock(**stock.dict())
    db.add(nuevo_stock)
    await db.commit()
    await db.refresh(nuevo_stock)
    result = await db.execute(
        select(Stock)
        .options(selectinload(Stock.producto))
        .options(selectinload(Stock.deposito))
        .options(selectinload(Stock.sucursal))
        .where(Stock.id == nuevo_stock.id)
    )
    stock_con_relacion = result.scalar_one()
    return stock_con_relacion """
    
    
async def crear_stock(db: AsyncSession, stock: StockCreateRequest):
    existing_stock = await db.execute(
        select(Stock).where(Stock.id_producto == stock.id_producto)
    )
    if existing_stock.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un registro de stock para el Producto con ID {stock.id_producto}. Si deseas modificarlo, usa el endpoint de actualización."
        )

    nuevo_stock = Stock(**stock.model_dump())
    db.add(nuevo_stock)
    await db.commit()
    await db.refresh(nuevo_stock)

    result = await db.execute(
        select(Stock)
        .options(selectinload(Stock.producto))
        .options(selectinload(Stock.deposito))
        .options(selectinload(Stock.sucursal))
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
