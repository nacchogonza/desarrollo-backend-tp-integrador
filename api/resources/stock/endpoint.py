from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.core import database
from .schemas import (
    StockResponse,
    StockCreateRequest,
    ReporteStockResumen,
    ReporteStockDetalle,
)

from .dal import obtener_stocks, crear_stock, delete_stock, reporte_stock_por_producto

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


""""
@router.get("/reporte_por_producto/{id_producto}", response_model=list[StockResponse], summary="Obtener reporte de stock por ID de producto (cantidad y ubicación)")
async def get_stock_report_by_product(id_producto: int, db: AsyncSession = Depends(database.get_db)): 
    reporte = await reporte_stock_por_producto(db, id_producto)
    if not reporte:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró stock para el producto con ID {id_producto}")
    return reporte """


@router.get(
    "/reportes/producto/{id_producto}",  # Cambié la ruta a '/reportes/producto/{id_producto}' para mayor claridad y consistencia
    response_model=ReporteStockResumen,  # <--- ¡Cambiado! Ahora usa tu schema de reporte
    summary="Obtener reporte de stock por ID de producto (cantidad y ubicación)",
    response_description="Reporte detallado del stock disponible para un producto dado, agrupado por ubicación en sucursales y depósitos.",
)
async def get_stock_report_by_product(
    id_producto: int,
    db: AsyncSession = Depends(database.get_db),  # <--- Usar database.get_db_session
):
    """
    Genera un reporte completo del stock de un producto específico, incluyendo la cantidad total
    y el desglose por cantidades en sucursales y depósitos.
    Requiere autenticación (ya cubierta por la dependencia del router).
    """
    # Tu DAL ya lanza HTTPException si el producto no se encuentra,
    # así que aquí solo tienes que llamar a la función.
    reporte_data_dict = await reporte_stock_por_producto(db, id_producto)

    # Mapea el diccionario retornado por tu DAL a tu modelo Pydantic ReporteStockResumen
    return ReporteStockResumen(**reporte_data_dict)
