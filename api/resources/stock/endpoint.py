from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import StockResponse, StockCreateRequest

from .dal import obtener_stocks, crear_stock, delete_stock, reporte_stock_por_producto

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

@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_endpoint(
    stock_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    was_deleted = await delete_stock(db, stock_id)
    if not was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock no encontrado para eliminar")
    return

@router.get("/reporte_por_producto/{id_producto}", response_model=list[StockResponse], summary="Obtener reporte de stock por ID de producto (cantidad y ubicación)")
async def get_stock_report_by_product(id_producto: int, db: AsyncSession = Depends(database.get_db)): 
    reporte = await reporte_stock_por_producto(db, id_producto)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró stock para el producto con ID {id_producto}")
    return reporte
