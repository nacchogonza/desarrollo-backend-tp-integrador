from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.resources.sucursal import dal
from api.core import database
from api.resources.sucursal.schemas import (
    SucursalResponse, 
    SucursalCreateRequest,
)

from ..auth.dal import get_current_active_user

router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)

async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model = list[SucursalResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_sucursales(db)

@router.post("/", response_model = SucursalResponse)
async def crear_sucursal(sucursal: SucursalCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_sucursal(db, sucursal)