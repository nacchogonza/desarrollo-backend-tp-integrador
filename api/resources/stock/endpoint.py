from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import (
    StockResponse,
    StockCreateRequest,
)

from .dal import obtener_stocks, crear_stock, delete_stock

from ..auth.dal import get_current_active_user

router = APIRouter(dependencies=[Depends(get_current_active_user)], tags=["Stock"])


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=list[StockResponse])
async def listarStocks(db: AsyncSession = Depends(get_db)):
    return await obtener_stocks(db)


@router.post("/", response_model=StockResponse)
async def crearStock(stock: StockCreateRequest, db: AsyncSession = Depends(get_db)):
    return await crear_stock(db, stock)


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_endpoint(stock_id: int, db: AsyncSession = Depends(get_db)):

    was_deleted = await delete_stock(db, stock_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock no encontrado para eliminar",
        )
    return
