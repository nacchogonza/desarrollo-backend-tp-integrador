from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.resources.proveedor import dal
from api.core import database
from api.resources.proveedor.schemas import (
    ProveedorResponse, 
    ProveedorCreateRequest, 
)

from ..auth.dal import get_current_active_user

router = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


async def get_db():
    async with database.AsyncSessionLocal() as session:
        yield session

@router.get("/", response_model= list[ProveedorResponse])
async def listar(db: AsyncSession = Depends(get_db)):
    return await dal.obtener_proveedor(db)

@router.post("/", response_model= ProveedorResponse)
async def crear_proveedor(proveedor: ProveedorCreateRequest, db: AsyncSession = Depends(get_db)):
    return await dal.crear_proveedor(db, proveedor)