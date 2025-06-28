from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from ..core.database import get_db
from .schemas import ReporteVentasResponse, ReporteClientesPorCiudadResponse
from . import dal as reports_dal
from ..resources.auth.dal import get_current_active_user


router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Reporte no disponible"}},
)


@router.get("/ventas", response_model=ReporteVentasResponse)
async def get_ventas_report_endpoint(
    fecha_inicio: date = Query(
        ...,
        description="Fecha de inicio para el reporte (YYYY-MM-DD)",
        example="2024-01-01",
    ),
    fecha_fin: date = Query(
        ...,
        description="Fecha de fin para el reporte (YYYY-MM-DD)",
        example="2024-01-31",
    ),
    db: AsyncSession = Depends(get_db),
):

    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin.",
        )

    report_data = await reports_dal.get_ventas_by_period(db, fecha_inicio, fecha_fin)

    if not report_data["detalles_ventas"]:

        pass

    return ReporteVentasResponse(**report_data)


@router.get("/clientes_por_ciudad", response_model=ReporteClientesPorCiudadResponse)
async def get_ventas_report_endpoint(
    id_ciudad: int,
    db: AsyncSession = Depends(get_db),
):

    if id == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID no puede ser 0",
        )

    report_data = await reports_dal.get_clientes_by_city(db, id_ciudad)

    if not report_data["clientes"]:

        pass

    return ReporteClientesPorCiudadResponse(**report_data)
