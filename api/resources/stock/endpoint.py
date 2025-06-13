from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import StockResponse, StockCreateRequest

from .dal import obtener_stocks, crear_stock

router = APIRouter()

async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session


@router.get("/", response_model=list[StockResponse])
async def listarStocks(db: AsyncSession = Depends(get_db)):
    return await obtener_stocks(db)


@router.post("/", response_model=StockResponse)
async def crearStock(stock: StockCreateRequest, db: AsyncSession = Depends(get_db)):
    return await crear_stock(db, stock)
